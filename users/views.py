from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from expenses.models import Expense

def home(request):
    """Landing page view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def signup(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
            
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('/')

@login_required
def profile(request):
    """User profile view."""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
        
    context = {
        'form': form,
        'total_expenses': Expense.objects.filter(user=request.user).count(),
    }
    return render(request, 'users/profile.html', context)