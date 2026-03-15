from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member, NextOfKin

class MemberRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    national_id = forms.CharField(max_length=20, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    
    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 
                 'national_id', 'address', 'profile_picture', 'password1', 'password2')
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Member.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone_number
    
    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if Member.objects.filter(national_id=national_id).exists():
            raise forms.ValidationError("This national ID is already registered.")
        return national_id

class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_picture')
    
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Member.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone_number

class NextOfKinForm(forms.ModelForm):
    class Meta:
        model = NextOfKin
        fields = ('name', 'relationship', 'phone_number', 'address', 'zone', 
                 'subcounty', 'parish', 'district', 'occupation')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }