from django.db import models
from django.utils import timezone
from django.db import transaction
from accounts.models import Account
from members.models import Member

class Deposit(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deposit of {self.amount} to account {self.account.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.amount <= 0:
            raise ValidationError("Deposit amount must be positive")

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Update account balance when deposit is made"""
        self.clean()
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:  # Only update balance for new deposits
            self.account.balance += self.amount
            self.account.save()

class Withdrawal(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Withdrawal of {self.amount} from account {self.account.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.amount <= 0:
            raise ValidationError("Withdrawal amount must be positive")
        if self.account.balance < self.amount:
            raise ValidationError("Insufficient balance for withdrawal")

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Update account balance when withdrawal is made"""
        self.clean()
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:  # Only update balance for new withdrawals
            self.account.balance -= self.amount
            self.account.save()

class Shares(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="member_shares")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date_purchased = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shares of {self.amount} for member {self.member.username}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.amount <= 0:
            raise ValidationError("Share amount must be positive")

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Update shares balance for the member's primary account"""
        self.clean()
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:  # Only update balance for new shares
            # Get member's primary account (first account or create one)
            primary_account = self.member.accounts.first()
            if primary_account:
                primary_account.shares_balance += self.amount
                primary_account.save()
        self.member.account.save()
