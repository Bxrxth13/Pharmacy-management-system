from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique medicine name
    dosage = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
     # Ensure this field exists

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Orders the medicines by name

class Stock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField()
    restock_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.medicine.name} - Quantity: {self.quantity}"

    class Meta:
        ordering = ['medicine']  # Orders stocks by medicine name

class WantedStock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='wanted_stocks')  # Add related_name for easier reverse lookups
    requested_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.medicine.name} - Requested Quantity: {self.requested_quantity}"

    class Meta:
        ordering = ['medicine']  # Orders wanted stocks by medicine name
