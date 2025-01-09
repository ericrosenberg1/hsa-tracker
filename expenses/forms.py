from django import forms
from .models import Expense, FamilyMember

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['family_member', 'payee', 'expense_date', 'amount', 'category', 'reimbursed', 'notes']
        widgets = {
            'family_member': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select family member'
            }),
            'payee': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter payee name'
            }),
            'expense_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter amount'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'reimbursed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter any additional notes'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields optional
        self.fields['family_member'].required = False
        self.fields['notes'].required = False
        
        # Add helpful labels
        self.fields['reimbursed'].label = "Has this expense been reimbursed?"
        
        # Add help text
        self.fields['amount'].help_text = "Enter the total amount in dollars"
        self.fields['category'].help_text = "Select the expense category"


class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['name', 'relationship', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter family member\'s name'
            }),
            'relationship': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select relationship'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Enter birth date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add helpful labels and text
        self.fields['relationship'].label = "Relationship to User"
        self.fields['relationship'].help_text = "E.g., Spouse, Child, Parent"
        self.fields['birth_date'].label = "Birth Date"
        self.fields['birth_date'].help_text = "Optional: Enter the family member's date of birth"
