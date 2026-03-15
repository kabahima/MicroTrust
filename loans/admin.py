from django.contrib import admin
from django.utils.html import format_html
from .models import Loan, LoanType, Fine, Repayment

@admin.register(LoanType)
class LoanTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'borrow_rate', 'description')
    search_fields = ('name',)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('member', 'loan_type', 'loan_amount', 'approved_amount', 'borrow_rate', 'status_display', 'remaining_balance_display', 'total_repayments', 'total_fines', 'date_applied')
    search_fields = ('member__username', 'member__first_name', 'member__last_name', 'loan_type__name')
    list_filter = ('status', 'loan_type', 'date_applied', 'date_approved')
    readonly_fields = ('date_applied', 'date_approved', 'date_paid_off', 'remaining_balance_display')
    filter_horizontal = ('fines', 'repayments')
    
    fieldsets = (
        ('Loan Information', {
            'fields': ('member', 'loan_type', 'loan_amount', 'borrow_rate', 'borrow_duration')
        }),
        ('Approval Details', {
            'fields': ('approved_amount', 'status', 'repayment_plan')
        }),
        ('Relationships', {
            'fields': ('fines', 'repayments'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('date_applied', 'date_approved', 'date_paid_off'),
            'classes': ('collapse',)
        }),
    )

    def status_display(self, obj):
        colors = {
            'pending': 'warning',
            'approved': 'success', 
            'paid_off': 'info',
            'rejected': 'danger'
        }
        color = colors.get(obj.status, 'secondary')
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())
    status_display.short_description = 'Status'

    def remaining_balance_display(self, obj):
        balance = obj.remaining_balance()
        if balance > 0:
            return format_html('<span style="color: red;">${:.2f}</span>', balance)
        else:
            return format_html('<span style="color: green;">Paid Off</span>')
    remaining_balance_display.short_description = 'Remaining Balance'

    def total_repayments(self, obj):
        count = obj.repayments.count()
        total = sum(r.amount_paid for r in obj.repayments.all())
        return format_html('{} (${:.2f})', count, total)
    total_repayments.short_description = 'Repayments'
    
    def total_fines(self, obj):
        unpaid_count = obj.fines.filter(is_paid=False).count()
        unpaid_total = sum(f.amount for f in obj.fines.filter(is_paid=False))
        if unpaid_count > 0:
            return format_html('<span style="color: red;">{} (${:.2f})</span>', unpaid_count, unpaid_total)
        return format_html('<span style="color: green;">None</span>')
    total_fines.short_description = 'Unpaid Fines'

    actions = ['approve_loans', 'reject_loans']

    def approve_loans(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(status='approved', date_approved=timezone.now())
        self.message_user(request, f'{updated} loans were approved.')
    approve_loans.short_description = "Approve selected loans"

    def reject_loans(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} loans were rejected.')
    reject_loans.short_description = "Reject selected loans"

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount', 'reason', 'fine_date', 'is_paid')
    list_filter = ('is_paid', 'fine_date')
    search_fields = ('loan__member__username', 'reason')
    readonly_fields = ('fine_date',)

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount_paid', 'repayment_date', 'is_fine_payment', 'payment_method')
    list_filter = ('is_fine_payment', 'payment_method', 'repayment_date')
    search_fields = ('loan__member__username', 'payment_method')
    readonly_fields = ('repayment_date',)
