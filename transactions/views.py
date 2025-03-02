from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Deposit, Withdrawal, Shares
from members.models import Account

# Deposit View
def deposit(request):
    if request.method == 'POST':
        account = Account.objects.get(member=request.user)  # Get the current user's account
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        
        # Create deposit transaction
        deposit = Deposit(account=account, amount=amount, description=description)
        deposit.save()

        messages.success(request, f"Deposited {amount} successfully!")
        return redirect('deposit')

    return render(request, 'transactions/deposit.html')

# Withdrawal View
def withdraw(request):
    if request.method == 'POST':
        account = Account.objects.get(member=request.user)  # Get the current user's account
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        # Create withdrawal transaction
        try:
            withdrawal = Withdrawal(account=account, amount=amount, description=description)
            withdrawal.save()
            messages.success(request, f"Withdrew {amount} successfully!")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('withdraw')

    return render(request, 'transactions/withdraw.html')

# Shares View
def shares(request):
    if request.method == 'POST':
        member = request.user  # Get the current member
        amount = request.POST.get('amount')

        # Create shares transaction
        shares = Shares(member=member, amount=amount)
        shares.save()

        messages.success(request, f"Purchased {amount} shares successfully!")
        return redirect('shares')

    return render(request, 'transactions/shares.html')
