# members/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member

class MemberRegistrationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Member
        fields = ['username', 'email', 'phone_number', 'national_id', 'address', 'profile_picture', 'password1', 'password2']
