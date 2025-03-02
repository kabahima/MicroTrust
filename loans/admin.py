from django.contrib import admin
from .models import Loan, Fine, Repayment

class LoanAdmin(admin.ModelAdmin):
    list_display = ('member', 'loan_type', 'loan_amount', 'approved_amount', 'borrow_rate', 'status', 'remaining_balance', 'date_applied', 'date_approved', 'date_paid_off')
    search_fields = ('member__username', 'loan_type__name')
    list_filter = ('status', 'loan_type')
    readonly_fields = ('remaining_balance', 'date_applied', 'date_approved', 'date_paid_off')  # Make remaining_balance and dates read-only in the form

    def remaining_balance(self, obj):
        """Display the remaining balance of the loan."""
        return obj.remaining_balance()
    remaining_balance.short_description = 'Remaining Balance'
    remaining_balance.admin_order_field = 'approved_amount'  # Allows sorting by remaining balance (optional)

    # Optional: Define the display for the "Repayment" and "Fine" count fields
    def total_repayments(self, obj):
        return obj.repayments.count()
    total_repayments.short_description = 'Total Repayments'
    
    def total_fines(self, obj):
        return obj.fines.filter(is_paid=False).count()  # Only unpaid fines
    total_fines.short_description = 'Unpaid Fines'

    # Add total repayments and fines to the list display
    list_display = ('member', 'loan_type', 'loan_amount', 'approved_amount', 'borrow_rate', 'status', 'remaining_balance', 'total_repayments', 'total_fines', 'date_applied', 'date_approved', 'date_paid_off')

# Register the Loan model with the customized admin
admin.site.register(Loan, LoanAdmin)

# Register other models (Fine, Repayment) as needed
admin.site.register(Fine)
admin.site.register(Repayment)
