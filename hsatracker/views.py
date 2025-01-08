from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import HSAExpense
from .forms import HSAExpenseForm


@login_required
def dashboard(request):
    """
    Display the user's HSA expense dashboard.
    Shows all expenses sorted by the most recent expense date.
    """
    expenses = HSAExpense.objects.filter(user=request.user).order_by('-expense_date')
    return render(request, 'dashboard.html', {'expenses': expenses})


@login_required
def add_expense(request):
    """
    Allow users to add a new HSA expense.
    Handles both GET (display form) and POST (submit form) requests.
    """
    if request.method == 'POST':
        form = HSAExpenseForm(request.POST)
        if form.is_valid():
            # Save the expense and assign it to the logged-in user
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
        else:
            # If the form contains errors, render the form with error messages
            return render(request, 'add_expense.html', {'form': form})
    else:
        # Provide a blank form for the user
        form = HSAExpenseForm()
    return render(request, 'add_expense.html', {'form': form})


@login_required
def edit_expense(request, expense_id):
    """
    Allow users to edit an existing HSA expense.
    Only the owner of the expense can edit it.
    """
    expense = get_object_or_404(HSAExpense, id=expense_id, user=request.user)

    if request.method == 'POST':
        form = HSAExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request, 'edit_expense.html', {'form': form, 'expense': expense})
    else:
        # Populate the form with the existing expense data
        form = HSAExpenseForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form, 'expense': expense})


@login_required
def delete_expense(request, expense_id):
    """
    Allow users to delete an HSA expense.
    Only the owner of the expense can delete it.
    """
    expense = get_object_or_404(HSAExpense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    
    # Confirm deletion on a GET request
    return render(request, 'confirm_delete.html', {'expense': expense})
