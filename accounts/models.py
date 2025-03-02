from django.db import models
import random

# AccountType model to allow manual creation of account types (e.g., savings, fixed)
class AccountType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# Account model to represent specific accounts
class Account(models.Model):
    account_number = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True, related_name="accounts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.account_type.name}) - {self.account_number}"

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        """Generate a unique 12-digit account number."""
        account_number = random.randint(100000000000, 999999999999)
        while Account.objects.filter(account_number=account_number).exists():
            account_number = random.randint(100000000000, 999999999999)
        return str(account_number)
