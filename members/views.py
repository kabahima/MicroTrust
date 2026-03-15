from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Member, NextOfKin
from accounts.models import Account, AccountType
from django.urls import reverse_lazy

# List of members - only for staff
class MemberListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Member
    template_name = 'members/member_list.html'
    context_object_name = 'members'
    permission_required = 'members.view_member'
    
    def get_queryset(self):
        return Member.objects.filter(is_approved=True)

# Create a new member - public registration
class MemberCreateView(CreateView):
    model = Member
    fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'national_id', 'address', 'profile_picture']
    template_name = 'members/member_form.html'
    success_url = reverse_lazy('members:registration_success')

    def form_valid(self, form):
        try:
            # Save the member instance (is_approved defaults to False)
            member = form.save(commit=False)
            member.is_approved = False  # Require admin approval
            member = form.save()

            # Create a default savings account for the member
            default_account_type, created = AccountType.objects.get_or_create(
                name='Savings',
                defaults={'description': 'Default savings account'}
            )
            
            account = Account.objects.create(
                name=f"{member.username} - Savings Account",
                account_type=default_account_type,
                description=f"Primary savings account for {member.username}"
            )
            member.accounts.add(account)

            # Process next of kin data
            next_of_kin_names = self.request.POST.getlist('next_of_kin_name')
            if next_of_kin_names:
                for i, name in enumerate(next_of_kin_names):
                    if name.strip():  # Only process non-empty names
                        relationship = self.request.POST.get(f'next_of_kin_relationship_{i}', '').strip()
                        phone_number = self.request.POST.get(f'next_of_kin_phone_number_{i}', '').strip()
                        address = self.request.POST.get(f'next_of_kin_address_{i}', '').strip()
                        zone = self.request.POST.get(f'next_of_kin_zone_{i}', '').strip()
                        subcounty = self.request.POST.get(f'next_of_kin_subcounty_{i}', '').strip()
                        parish = self.request.POST.get(f'next_of_kin_parish_{i}', '').strip()
                        district = self.request.POST.get(f'next_of_kin_district_{i}', '').strip()
                        occupation = self.request.POST.get(f'next_of_kin_occupation_{i}', '').strip()

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

            messages.success(self.request, 'Registration successful! Your account is pending approval.')
            return super().form_valid(form)
            
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, 'An error occurred during registration. Please try again.')
            return self.form_invalid(form)

# Update member details - only for staff or the member themselves
class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_picture']
    template_name = 'members/member_form.html'

    def get_success_url(self):
        # If editing own profile, redirect to profile page
        if 'pk' not in self.kwargs or self.kwargs['pk'] == str(self.request.user.pk):
            return reverse_lazy('members:profile')
        else:
            # If staff editing another member, redirect to member list
            return reverse_lazy('members:member_list')

    def get_object(self):
        # Staff can edit any member, regular users can only edit themselves
        if 'pk' in self.kwargs:
            # Editing another member (staff only)
            if self.request.user.has_perm('members.change_member'):
                return get_object_or_404(Member, pk=self.kwargs['pk'])
            else:
                # Non-staff trying to edit another member - redirect to own profile
                return get_object_or_404(Member, pk=self.request.user.pk)
        else:
            # Editing own profile (no pk in URL)
            return get_object_or_404(Member, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_profile'] = 'pk' not in self.kwargs or self.kwargs.get('pk') == str(self.request.user.pk)
        context['next_of_kin'] = NextOfKin.objects.filter(member=self.object)
        return context

    def form_valid(self, form):
        try:
            member = form.save()

            # Update next of kin data
            next_of_kin_names = self.request.POST.getlist('next_of_kin_name')
            if next_of_kin_names:
                # Clear existing next of kin for this member
                NextOfKin.objects.filter(member=member).delete()
                
                for i, name in enumerate(next_of_kin_names):
                    if name.strip():  # Only process non-empty names
                        relationship = self.request.POST.get(f'next_of_kin_relationship_{i}', '').strip()
                        phone_number = self.request.POST.get(f'next_of_kin_phone_number_{i}', '').strip()
                        address = self.request.POST.get(f'next_of_kin_address_{i}', '').strip()
                        zone = self.request.POST.get(f'next_of_kin_zone_{i}', '').strip()
                        subcounty = self.request.POST.get(f'next_of_kin_subcounty_{i}', '').strip()
                        parish = self.request.POST.get(f'next_of_kin_parish_{i}', '').strip()
                        district = self.request.POST.get(f'next_of_kin_district_{i}', '').strip()
                        occupation = self.request.POST.get(f'next_of_kin_occupation_{i}', '').strip()

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

            messages.success(self.request, 'Profile updated successfully!')
            return super().form_valid(form)
            
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, 'An error occurred while updating. Please try again.')
            return self.form_invalid(form)

@login_required
def profile_view(request):
    """View for members to see their own profile"""
    member = get_object_or_404(Member, pk=request.user.pk)
    next_of_kin = NextOfKin.objects.filter(member=member)
    accounts = member.accounts.all()
    
    context = {
        'member': member,
        'next_of_kin': next_of_kin,
        'accounts': accounts,
    }
    return render(request, 'members/profile.html', context)

@login_required
def account_card(request):
    """View for members to print their account card"""
    member = get_object_or_404(Member, pk=request.user.pk)
    accounts = member.accounts.all()
    
    context = {
        'member': member,
        'accounts': accounts,
    }
    return render(request, 'members/account_card.html', context)

def registration_success(request):
    """Success page after registration"""
    return render(request, 'members/registration_success.html')