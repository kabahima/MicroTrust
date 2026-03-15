from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

def home(request):
    context = {}
    
    if request.user.is_authenticated:
        # Get user's active loans count
        try:
            active_loans_count = request.user.loan_set.filter(status='approved').count()
            total_loan_amount = request.user.loan_set.filter(status='approved').aggregate(
                total=Sum('approved_amount'))['total'] or 0
        except AttributeError:
            active_loans_count = 0
            total_loan_amount = 0
        
        # Get user's accounts with transaction summaries
        user_accounts = request.user.accounts.all()
        
        # Get recent transactions
        recent_deposits = []
        recent_withdrawals = []
        recent_shares = []
        
        if user_accounts.exists():
            primary_account = user_accounts.first()
            recent_deposits = primary_account.deposits.all()[:5]
            recent_withdrawals = primary_account.withdrawals.all()[:5]
            
            # Get transaction statistics
            thirty_days_ago = timezone.now() - timedelta(days=30)
            monthly_deposits = primary_account.deposits.filter(
                created_at__gte=thirty_days_ago
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            monthly_withdrawals = primary_account.withdrawals.filter(
                created_at__gte=thirty_days_ago
            ).aggregate(total=Sum('amount'))['total'] or 0
        else:
            primary_account = None
            monthly_deposits = 0
            monthly_withdrawals = 0
        
        # Get recent shares
        recent_shares = request.user.member_shares.all()[:5]
        total_shares_value = request.user.member_shares.aggregate(
            total=Sum('amount'))['total'] or 0
        
        context.update({
            'active_loans_count': active_loans_count,
            'total_loan_amount': total_loan_amount,
            'primary_account': primary_account,
            'user_accounts': user_accounts,
            'recent_deposits': recent_deposits,
            'recent_withdrawals': recent_withdrawals,
            'recent_shares': recent_shares,
            'total_shares_value': total_shares_value,
            'monthly_deposits': monthly_deposits,
            'monthly_withdrawals': monthly_withdrawals,
        })
    
    return render(request, 'home.html', context)
