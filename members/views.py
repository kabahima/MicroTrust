from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from .models import Member, NextOfKin
from django.urls import reverse_lazy

# List of members
class MemberListView(ListView):
    model = Member
    template_name = 'members/member_list.html'  # Create this template
    context_object_name = 'members'

# Create a new member
class MemberCreateView(CreateView):
    model = Member
    fields = ['username', 'phone_number', 'national_id', 'address', 'profile_picture', 'is_approved']
    template_name = 'members/member_form.html'  # Create this template
    success_url = reverse_lazy('members:member_list')  # Redirect after creating a member

    def form_valid(self, form):
        # Save the member instance
        member = form.save()

        # Optionally add next of kin, if provided
        next_of_kin_data = self.request.POST.getlist('next_of_kin_name')
        if next_of_kin_data:
            for i, name in enumerate(next_of_kin_data):
                # Gather other necessary fields for each next of kin
                relationship = self.request.POST.get(f'next_of_kin_relationship_{i}', '')
                phone_number = self.request.POST.get(f'next_of_kin_phone_number_{i}', '')
                address = self.request.POST.get(f'next_of_kin_address_{i}', '')
                zone = self.request.POST.get(f'next_of_kin_zone_{i}', '')
                subcounty = self.request.POST.get(f'next_of_kin_subcounty_{i}', '')
                parish = self.request.POST.get(f'next_of_kin_parish_{i}', '')
                district = self.request.POST.get(f'next_of_kin_district_{i}', '')
                occupation = self.request.POST.get(f'next_of_kin_occupation_{i}', '')

                # Create NextOfKin object
                NextOfKin.objects.create(
                    member=member,
                    name=name,
                    relationship=relationship,
                    phone_number=phone_number,
                    address=address,
                    zone=zone,
                    subcounty=subcounty,
                    parish=parish,
                    district=district,
                    occupation=occupation,
                )

        return super().form_valid(form)

# Update member details
class MemberUpdateView(UpdateView):
    model = Member
    fields = ['username', 'phone_number', 'national_id', 'address', 'profile_picture', 'is_approved']
    template_name = 'members/member_form.html'  # Create this template
    success_url = reverse_lazy('members:member_list')  # Redirect after updating a member

    def form_valid(self, form):
        # Save the member instance
        member = form.save()

        # Update or add next of kin, if provided
        next_of_kin_data = self.request.POST.getlist('next_of_kin_name')
        if next_of_kin_data:
            for i, name in enumerate(next_of_kin_data):
                # Gather other necessary fields for each next of kin
                relationship = self.request.POST.get(f'next_of_kin_relationship_{i}', '')
                phone_number = self.request.POST.get(f'next_of_kin_phone_number_{i}', '')
                address = self.request.POST.get(f'next_of_kin_address_{i}', '')
                zone = self.request.POST.get(f'next_of_kin_zone_{i}', '')
                subcounty = self.request.POST.get(f'next_of_kin_subcounty_{i}', '')
                parish = self.request.POST.get(f'next_of_kin_parish_{i}', '')
                district = self.request.POST.get(f'next_of_kin_district_{i}', '')
                occupation = self.request.POST.get(f'next_of_kin_occupation_{i}', '')

                # Update or create next of kin object (checks if the next of kin exists)
                NextOfKin.objects.update_or_create(
                    member=member,
                    name=name,
                    defaults={
                        'relationship': relationship,
                        'phone_number': phone_number,
                        'address': address,
                        'zone': zone,
                        'subcounty': subcounty,
                        'parish': parish,
                        'district': district,
                        'occupation': occupation,
                    }
                )

        return super().form_valid(form)
