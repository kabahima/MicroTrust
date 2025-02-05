# members/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from cloudinary.models import CloudinaryField
import random

class Member(AbstractUser):
    account_number = models.CharField(max_length=12, unique=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    profile_picture = CloudinaryField('image', default='default_profile.png')
    is_approved = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name="member_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="member_permissions", blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        """Generate a unique 12-digit account number."""
        account_number = random.randint(100000000000, 999999999999)
        while Member.objects.filter(account_number=account_number).exists():
            account_number = random.randint(100000000000, 999999999999)
        return str(account_number)
