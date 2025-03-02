# forms.py
from django import forms
from .models import Member, NextOfKin

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'phone_number', 'national_id', 'address', 'profile_picture', 'is_approved']

class NextOfKinForm(forms.ModelForm):
    class Meta:
        model = NextOfKin
        fields = ['name', 'relationship', 'phone_number', 'address', 'zone', 'subcounty', 'parish', 'district', 'occupation']
