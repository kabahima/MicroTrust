from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Import UserAdmin here
from .models import Member, NextOfKin

# Inline model admin for NextOfKin
class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 1  # Number of empty forms to show by default

# MemberAdmin with inline for NextOfKin
class MemberAdmin(UserAdmin):  # Ensure this extends UserAdmin
    model = Member
    list_display = ('username', 'phone_number', 'national_id', 'is_approved', 'account_number')
    list_filter = ('is_approved',)
    search_fields = ('username', 'phone_number', 'national_id')
    filter_horizontal = ('accounts',)
    
    # Add inline for next of kin details
    inlines = [NextOfKinInline]

    # Optionally customize the fields shown in the form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'national_id', 'address', 'profile_picture', 'is_approved', 'accounts')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'national_id', 'address', 'profile_picture', 'is_approved', 'accounts')}),
    )


admin.site.register(Member, MemberAdmin)
admin.site.register(NextOfKin)
