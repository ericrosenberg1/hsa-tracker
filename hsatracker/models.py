from django.db import models
from django.conf import settings

class HSAExpense(models.Model):
    CATEGORY_CHOICES = [
        ('medical', 'Medical'),
        ('dental', 'Dental'),
        ('vision', 'Vision'),
        ('prescription', 'Prescription'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payee = models.CharField(max_length=100)
    expense_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    reimbursed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.payee} - ${self.amount}"
