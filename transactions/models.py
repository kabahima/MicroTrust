from django.db import models
from django.utils import timezone
from accounts.models import Account  # Correct import for Account model
from members.models import Member  # Import Member model if needed

class Deposit(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="deposits")  # Correct ForeignKey reference
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Deposit of {self.amount} to account {self.account.member.username}"

    def save(self, *args, **kwargs):
        """ Update account balance when deposit is made """
        super().save(*args, **kwargs)
        self.account.balance += self.amount
        self.account.save()

class Withdrawal(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="withdrawals")  # Correct ForeignKey reference
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Withdrawal of {self.amount} from account {self.account.member.username}"

    def save(self, *args, **kwargs):
        """ Update account balance when withdrawal is made """
        super().save(*args, **kwargs)
        if self.account.balance >= self.amount:
            self.account.balance -= self.amount
            self.account.save()
        else:
            raise ValueError("Insufficient balance for withdrawal")

class Shares(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="shares")  # Correct ForeignKey reference to Member
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date_purchased = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Shares of {self.amount} for member {self.member.username}"

    def save(self, *args, **kwargs):
        """ Update shares balance for the member """
        super().save(*args, **kwargs)
        self.member.account.shares_balance += self.amount
        self.member.account.save()
