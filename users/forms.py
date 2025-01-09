# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, FamilyMember

class CustomUserCreationForm(UserCreationForm):
   class Meta(UserCreationForm.Meta):
       model = CustomUser
       fields = ('email',)

   def clean_email(self):
       email = self.cleaned_data.get('email')
       if CustomUser.objects.filter(email=email).exists():
           raise forms.ValidationError('This email is already in use.')
       return email

class CustomUserChangeForm(UserChangeForm):
   password = None
   
   class Meta:
       model = CustomUser
       fields = ('email',)

class FamilyMemberForm(forms.ModelForm):
   class Meta:
       model = FamilyMember
       fields = ['name', 'relationship']