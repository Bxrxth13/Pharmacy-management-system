# pharmacy/management/commands/create_stock.py

from django.core.management.base import BaseCommand
from pharmacy.models import Medicine, Stock

class Command(BaseCommand):
    help = 'Create stock for a specific medicine'

    def handle(self, *args, **kwargs):
        try:
            # Get the medicine instance (you can adjust the ID as needed)
            medicine = Medicine.objects.get(id=1)  # Change ID if necessary
            stock = Stock(medicine=medicine, quantity=100, restock_date='2024-10-19')
            stock.save()  # Save the stock entry
            self.stdout.write(self.style.SUCCESS('Stock created successfully.'))
        except Medicine.DoesNotExist:
            self.stdout.write(self.style.ERROR('Medicine matching query does not exist.'))
