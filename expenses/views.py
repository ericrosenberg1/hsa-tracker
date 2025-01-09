"""Views for managing expenses and family members."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Expense, FamilyMember
from .forms import ExpenseForm, FamilyMemberForm


@login_required
def dashboard(request):
    """Dashboard view showing expense summary and list."""
    expenses = Expense.objects.filter(user=request.user).order_by('-expense_date')
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    pending_reimbursement = expenses.filter(reimbursed=False).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'pending_reimbursement': pending_reimbursement,
    }
    return render(request, 'expenses/dashboard.html', context)

@login_required
def expense_list(request):
    """View to list all expenses."""
    expenses = Expense.objects.filter(user=request.user).order_by('-expense_date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def add_expense(request):
    """Add new expense."""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    context = {
        'form': form,
        'form_title': 'Add Expense',  # Optional title for the form
    }
    return render(request, 'expenses/form.html', context)

@login_required
def edit_expense(request, expense_id):
    """Edit an existing expense."""
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)

    context = {
        'form': form,
        'form_title': 'Edit Expense',  # Optional title for customization
    }
    return render(request, 'expenses/form.html', context)

@login_required
def delete_expense(request, expense_id):
    """Delete expense with confirmation."""
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
        return redirect('dashboard')

    context = {'expense': expense}
    return render(request, 'expenses/confirm_delete.html', context)

@login_required
def family(request):
    """Family members list view."""
    family_members = FamilyMember.objects.filter(user=request.user).order_by('name')
    return render(request, 'expenses/family.html', {'family_members': family_members})

@login_required
def add_family_member(request):
    """Add new family member."""
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            messages.success(request, 'Family member added successfully.')
            return redirect('family')
    else:
        form = FamilyMemberForm()

    return render(request, 'expenses/family_form.html', {'form': form})


@login_required
def edit_family_member(request, member_id):
    """Edit existing family member."""
    member = get_object_or_404(FamilyMember, id=member_id, user=request.user)

    if request.method == 'POST':
        form = FamilyMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family member updated successfully.')
            return redirect('family')
    else:
        form = FamilyMemberForm(instance=member)

    return render(request, 'expenses/family_form.html', {'form': form})


@login_required
def delete_family_member(request, member_id):
    """Delete family member with confirmation."""
    member = get_object_or_404(FamilyMember, id=member_id, user=request.user)

    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Family member deleted successfully.')
        return redirect('family')

    return render(request, 'expenses/family_confirm_delete.html', {'family_member': member})
