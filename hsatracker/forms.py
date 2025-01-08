from django import forms
from .models import HSAExpense

class HSAExpenseForm(forms.ModelForm):
    class Meta:
        model = HSAExpense
        fields = ['payee', 'expense_date', 'amount', 'category', 'reimbursed']
