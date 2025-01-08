from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import HSAExpense

def home(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    return render(request, 'users/home.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('users:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

@login_required
def dashboard(request):
    expenses = HSAExpense.objects.filter(family_member=request.user).order_by('-expense_date')
    total_expenses = sum(expense.total for expense in expenses)
    return render(request, 'users/dashboard.html', {
        'expenses': expenses,
        'total_expenses': total_expenses
    })