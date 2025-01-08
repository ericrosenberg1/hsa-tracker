from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User model with additional fields for family members.
    """
    is_family_member = models.BooleanField(
        default=False,
        help_text="Indicates if the user is a family member."
    )
    family_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Name of the family member (if applicable)."
    )
    relationship = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Relationship to the primary user (e.g., spouse, child)."
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="A short bio for the user."
    )

    def __str__(self):
        return self.family_name if self.is_family_member else self.username


class HSAExpense(models.Model):
    """
    Model to store HSA expenses.
    """
    CATEGORY_CHOICES = [
        ('Pharmacy', 'Pharmacy'),
        ('Medical', 'Medical'),
        ('Dental', 'Dental'),
        ('Vision', 'Vision'),
        ('Lab Testing', 'Lab Testing'),
        ('Other', 'Other'),
    ]

    payee = models.CharField(
        max_length=100,
        help_text="The name of the payee."
    )
    expense_date = models.DateField(
        help_text="The date the expense was incurred."
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total amount of the expense."
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        help_text="Category of the expense."
    )
    family_member = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="family_expenses",
        help_text="The family member associated with this expense."
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or details about the expense."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the expense was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the expense was last updated."
    )

    def __str__(self):
        return f"{self.payee} - ${self.total:.2f} ({self.category})"
