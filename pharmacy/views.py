from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine, Stock, WantedStock

def home(request):
    return render(request, 'pharmacy/home.html')


def medicine_list(request):
    # Fetch all medicines and prefetch related stock entries
    medicines = Medicine.objects.prefetch_related('stocks').all()
    
    # Prepare data to include stock quantities
    medicine_data = []
    for medicine in medicines:
        # Get the first stock entry for each medicine
        stock_entry = medicine.stocks.first()
        stock_quantity = stock_entry.quantity if stock_entry else 0
        medicine_data.append({
            'medicine': medicine,
            'stock_quantity': stock_quantity
        })

    return render(request, 'pharmacy/medicine_list.html', {'medicines': medicine_data})

def add_medicine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dosage = request.POST.get('dosage')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        # Validate inputs
        if not all([name, dosage, price, quantity]):
            error_message = "All fields are required."
            return render(request, 'pharmacy/add_medicine.html', {'error': error_message})

        try:
            price = float(price)
            quantity = int(quantity)

            # Create or update the medicine
            medicine, created = Medicine.objects.get_or_create(name=name, defaults={'dosage': dosage, 'price': price})
            if not created:
                # Update existing medicine
                medicine.dosage = dosage
                medicine.price = price
                medicine.save()

            # Create or update stock
            stock, created = Stock.objects.get_or_create(medicine=medicine, defaults={'quantity': 0})
            stock.quantity += quantity  # Update stock quantity
            stock.save()

            # Update the quantity in the Medicine model if necessary
            medicine.quantity += quantity  # Only if you want to keep track in Medicine
            medicine.save()

            # Check if stock is low and add to wanted stock
            if stock.quantity <= 2:
                wanted_stock, _ = WantedStock.objects.get_or_create(medicine=medicine)
                wanted_stock.requested_quantity = 10  # Adjust as needed
                wanted_stock.save()

            return redirect('medicine_list')
        except ValueError:
            error_message = "Price must be a valid number and quantity must be a valid integer."
            return render(request, 'pharmacy/add_medicine.html', {'error': error_message})

    return render(request, 'pharmacy/add_medicine.html')

def edit_medicine(request, id):  # Accept 'id' as a parameter
    medicine = get_object_or_404(Medicine, pk=id)
    
    # Ensure stock is retrieved as a single object
    stock, _ = Stock.objects.get_or_create(medicine=medicine)  # get_or_create returns a tuple, hence unpack

    if request.method == 'POST':
        name = request.POST.get('name')
        dosage = request.POST.get('dosage')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')  # New quantity field

        if not all([name, dosage, price]):
            error_message = "All fields except quantity are required."
            return render(request, 'pharmacy/edit.html', {'medicine': medicine, 'error': error_message})

        try:
            price = float(price)
            medicine.name = name
            medicine.dosage = dosage
            medicine.price = price
            medicine.save()

            # Update stock quantity if provided
            if quantity and quantity.isdigit():
                quantity = int(quantity)
                quantity_difference = quantity - stock.quantity
                stock.quantity += quantity_difference
                stock.save()

            return redirect('medicine_list')
        except ValueError:
            error_message = "Price must be a valid number."
            return render(request, 'pharmacy/edit.html', {'medicine': medicine, 'error': error_message})

    return render(request, 'pharmacy/edit.html', {'medicine': medicine, 'stock_quantity': stock.quantity})

def delete_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)

    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')

    return render(request, 'pharmacy/delete.html', {'medicine': medicine})

def wanted_stock(request):
    low_stock_threshold = 5
    medicines = Stock.objects.filter(quantity__lt=low_stock_threshold)
    return render(request, 'pharmacy/wanted_stock.html', {'medicines': medicines})

def add_stock(request):
    if request.method == 'POST':
        medicine_id = request.POST.get('medicine_id')
        quantity = request.POST.get('quantity')

        # Validate quantity
        if not quantity.isdigit() or int(quantity) <= 0:
            error_message = "Quantity must be a positive integer."
            medicines = Medicine.objects.all()
            return render(request, 'pharmacy/add_stock.html', {'medicines': medicines, 'error': error_message})

        # Retrieve the medicine object or return a 404 error if not found
        medicine = get_object_or_404(Medicine, id=medicine_id)

        # Use get_or_create to avoid MultipleObjectsReturned
        stock, created = Stock.objects.get_or_create(medicine=medicine, defaults={'quantity': 0})

        # Update the quantity
        stock.quantity += int(quantity)
        stock.save()

        # Also update the quantity in the Medicine model if necessary
        medicine.quantity += int(quantity)  # Only if you want to keep track in Medicine
        medicine.save()

        return redirect('wanted_stock')  # Redirect after successful stock addition

    # GET request handling
    medicines = Medicine.objects.all()
    return render(request, 'pharmacy/add_stock.html', {'medicines': medicines})  #the quantity of the medicine is not updating please rectify it. 