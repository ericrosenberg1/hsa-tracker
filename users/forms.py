from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, HSAExpense

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    family_name = forms.CharField(max_length=50, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

class CustomUserChangeForm(UserChangeForm):
    password = None
    email = forms.EmailField(required=True)
    family_name = forms.CharField(max_length=50, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'family_name', 'bio')

class HSAExpenseForm(forms.ModelForm):
    class Meta:
        model = HSAExpense
        fields = ['payee', 'expense_date', 'total', 'category', 'notes']
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }