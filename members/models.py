from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from cloudinary.models import CloudinaryField
from accounts.models import Account  
import random

class Member(AbstractUser):
    account_number = models.CharField(max_length=12, unique=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    profile_picture = CloudinaryField('image', default='default_profile.png')
    is_approved = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name="member_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="member_permissions", blank=True)
    
    # Many-to-many relationship with Account from the accounts app
    accounts = models.ManyToManyField(Account, related_name="members", blank=True)

    def __str__(self):
        return f"{self.username} ({self.phone_number})"  # Adjusted for more useful representation

    def save(self, *args, **kwargs):
        # Automatically generate an account number if not provided
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        """Generate a unique 12-digit account number."""
        account_number = random.randint(100000000000, 999999999999)
        while Member.objects.filter(account_number=account_number).exists():
            account_number = random.randint(100000000000, 999999999999)
        return str(account_number)


class NextOfKin(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    zone = models.CharField(max_length=255, null=True, blank=True)
    subcounty = models.CharField(max_length=255, null=True, blank=True)
    parish = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.relationship}'
