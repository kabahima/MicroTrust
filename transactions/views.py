from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal, InvalidOperation
from .models import Deposit, Withdrawal, Shares
from accounts.models import Account
from members.models import Member

@login_required
def deposit(request):
    # Get member and account info
    member = get_object_or_404(Member, id=request.user.id)
    primary_account = member.accounts.first()
    
    if request.method == 'POST':
        try:
            if not member.is_approved:
                messages.error(request, "Your account is not approved for transactions.")
                return redirect('transactions:deposit')
            
            if not primary_account:
                messages.error(request, "No account found. Please contact administrator.")
                return redirect('transactions:deposit')
            
            # Validate and convert amount
            amount_str = request.POST.get('amount', '').strip()
            if not amount_str:
                messages.error(request, "Amount is required.")
                return redirect('transactions:deposit')
            
            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    messages.error(request, "Amount must be positive.")
                    return redirect('transactions:deposit')
            except (InvalidOperation, ValueError):
                messages.error(request, "Invalid amount format.")
                return redirect('transactions:deposit')
            
            description = request.POST.get('description', '').strip()
            
            # Create deposit transaction
            with transaction.atomic():
                deposit_obj = Deposit(account=primary_account, amount=amount, description=description)
                deposit_obj.save()

            messages.success(request, f"Deposited {amount} successfully!")
            return redirect('transactions:deposit')
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('transactions:deposit')
        except Exception as e:
            messages.error(request, "An error occurred. Please try again.")
            return redirect('transactions:deposit')

    context = {
        'primary_account': primary_account,
    }
    return render(request, 'transactions/deposit.html', context)

@login_required
def withdraw(request):
    # Get member and account info
    member = get_object_or_404(Member, id=request.user.id)
    primary_account = member.accounts.first()
    
    if request.method == 'POST':
        try:
            if not member.is_approved:
                messages.error(request, "Your account is not approved for transactions.")
                return redirect('transactions:withdraw')
            
            if not primary_account:
                messages.error(request, "No account found. Please contact administrator.")
                return redirect('transactions:withdraw')
            
            # Validate and convert amount
            amount_str = request.POST.get('amount', '').strip()
            if not amount_str:
                messages.error(request, "Amount is required.")
                return redirect('transactions:withdraw')
            
            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    messages.error(request, "Amount must be positive.")
                    return redirect('transactions:withdraw')
            except (InvalidOperation, ValueError):
                messages.error(request, "Invalid amount format.")
                return redirect('transactions:withdraw')
            
            description = request.POST.get('description', '').strip()

            # Create withdrawal transaction
            with transaction.atomic():
                withdrawal_obj = Withdrawal(account=primary_account, amount=amount, description=description)
                withdrawal_obj.save()

            messages.success(request, f"Withdrew {amount} successfully!")
            return redirect('transactions:withdraw')
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('transactions:withdraw')
        except Exception as e:
            messages.error(request, "An error occurred. Please try again.")
            return redirect('transactions:withdraw')

    context = {
        'primary_account': primary_account,
    }
    return render(request, 'transactions/withdraw.html', context)

@login_required
def shares(request):
    # Get member info
    member = get_object_or_404(Member, id=request.user.id)
    primary_account = member.accounts.first()
    
    if request.method == 'POST':
        try:
            if not member.is_approved:
                messages.error(request, "Your account is not approved for share purchases.")
                return redirect('transactions:shares')
            
            # Validate and convert amount
            amount_str = request.POST.get('amount', '').strip()
            if not amount_str:
                messages.error(request, "Amount is required.")
                return redirect('transactions:shares')
            
            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    messages.error(request, "Amount must be positive.")
                    return redirect('transactions:shares')
            except (InvalidOperation, ValueError):
                messages.error(request, "Invalid amount format.")
                return redirect('transactions:shares')

            # Create shares transaction
            with transaction.atomic():
                shares_obj = Shares(member=member, amount=amount)
                shares_obj.save()

            messages.success(request, f"Purchased shares worth {amount} successfully!")
            return redirect('transactions:shares')
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('transactions:shares')
        except Exception as e:
            messages.error(request, "An error occurred. Please try again.")
            return redirect('transactions:shares')

    context = {
        'primary_account': primary_account,
    }
    return render(request, 'transactions/shares.html', context)
