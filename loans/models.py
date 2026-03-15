from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class LoanType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    borrow_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)  # Default borrow rate

    def __str__(self):
        return self.name

class Loan(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    loan_type = models.ForeignKey('LoanType', on_delete=models.SET_NULL, null=True, blank=True)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    borrow_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)  # Default rate, can be overridden by loan type
    borrow_duration = models.IntegerField()  # Duration in months
    approved_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('paid_off', 'Paid Off'), ('rejected', 'Rejected')], default='pending')
    repayment_plan = models.TextField(null=True, blank=True)  # Store repayment plan details
    date_applied = models.DateTimeField(default=timezone.now)
    date_approved = models.DateTimeField(null=True, blank=True)
    date_paid_off = models.DateTimeField(null=True, blank=True)

    # Link to repayments and fines
    fines = models.ManyToManyField('Fine', related_name="loan_fines", blank=True)
    repayments = models.ManyToManyField('Repayment', related_name="loan_repayments", blank=True)

    def __str__(self):
        return f"Loan for {self.member.username} - {self.loan_type.name if self.loan_type else 'No Type'}"

    def save(self, *args, **kwargs):
        """Override save method to handle borrow rate and approved amount."""
        if self.loan_type:
            self.borrow_rate = self.loan_type.borrow_rate  # Set borrow rate from loan type

        if not self.approved_amount:
            self.approved_amount = self.loan_amount  # Default logic, can be customized

        if self.status == 'approved' and not self.date_approved:
            self.date_approved = timezone.now()
        if self.status == 'paid_off' and not self.date_paid_off:
            self.date_paid_off = timezone.now()

        super().save(*args, **kwargs)

    def calculate_total_repayment(self):
        """Calculate the total repayment amount based on loan + interest."""
        return self.approved_amount * (1 + self.borrow_rate / 100)

    def apply_fine(self, overdue_days, reason="Late payment"):
        """Apply fine if overdue and update the fine-related fields."""
        fine = Fine.objects.create(
            loan=self,
            amount=self.loan_amount * 0.01 * overdue_days,  # 1% of loan amount per overdue day
            reason=reason,
        )
        self.fines.add(fine)

    def remaining_balance(self):
        """Calculate the remaining balance including interest and fines, minus repayments."""
        total_loan_with_interest = self.calculate_total_repayment()
        total_repaid = sum([repayment.amount_paid for repayment in self.repayments.all()])
        total_unpaid_fines = sum([fine.amount for fine in self.fines.filter(is_paid=False)])
        return total_loan_with_interest + total_unpaid_fines - total_repaid

    remaining_balance.short_description = 'Remaining Balance'
   




class Fine(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name="loan_fines")  # Added related_name here
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    reason = models.TextField(null=True, blank=True)
    fine_date = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)  # Track whether the fine has been paid off

    def __str__(self):
        return f"Fine of {self.amount} for loan {self.loan.id} - {self.reason}"

    def mark_as_paid(self):
        """Method to mark the fine as paid."""
        self.is_paid = True
        self.save()

    def save(self, *args, **kwargs):
        """Override save to ensure fine is only applied if overdue."""
        super().save(*args, **kwargs)


# class Repayment(models.Model):
#     loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name="loan_repayments")  # Added related_name here
#     amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
#     repayment_date = models.DateTimeField(default=timezone.now)
#     is_fine_payment = models.BooleanField(default=False)  # Track if the payment was for fines
#     payment_method = models.CharField(max_length=255, null=True, blank=True)  # e.g., Cash, Bank Transfer, Mobile Payment
#     notes = models.TextField(null=True, blank=True)  # Additional details like partial repayment, etc.

#     def __str__(self):
#         return f"Repayment of {self.amount_paid} on loan {self.loan.id} on {self.repayment_date}"

#     def save(self, *args, **kwargs):
#         """Override save method to update loan status after payment."""
#         # Example: Deduct fine amount from loan when fine is paid
#         if self.is_fine_payment:
#             fine = self.loan.fines.filter(is_paid=False).first()
#             if fine and self.amount_paid >= fine.amount:
#                 fine.mark_as_paid()  # Mark the fine as paid if the payment covers it
#         super().save(*args, **kwargs)


class Repayment(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name="loan_repayments")
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    repayment_date = models.DateTimeField(default=timezone.now)
    is_fine_payment = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Repayment of {self.amount_paid} on loan {self.loan.id} on {self.repayment_date}"

    def save(self, *args, **kwargs):
        """Override save method to update loan status after payment."""
        # Example: Deduct fine amount from loan when fine is paid
        if self.is_fine_payment:
            fine = self.loan.fines.filter(is_paid=False).first()
            if fine and self.amount_paid >= fine.amount:
                fine.mark_as_paid()  # Mark the fine as paid if the payment covers it
        super().save(*args, **kwargs)
        self.loan.save()  # Ensure the loan object is saved again to recalculate remaining balance
