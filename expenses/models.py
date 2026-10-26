from django.db import models

# Create your models here.
class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.title

class Budget(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=5000)

    def __str__(self):
        return f"Monthly Budget: {self.amount}"
