from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Member, NextOfKin

# Inline model admin for NextOfKin
class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 0
    fields = ('name', 'relationship', 'phone_number', 'district')
    readonly_fields = ('name', 'relationship', 'phone_number')

# Enhanced MemberAdmin
@admin.register(Member)
class MemberAdmin(UserAdmin):
    model = Member
    list_display = ('username', 'get_full_name', 'phone_number', 'account_number', 'approval_status', 'date_joined', 'account_balance')
    list_filter = ('is_approved', 'is_active', 'date_joined', 'accounts__account_type')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'national_id', 'email')
    filter_horizontal = ('accounts', 'groups', 'user_permissions')
    readonly_fields = ('date_joined', 'last_login', 'account_number', 'get_profile_picture')
    
    # Add inline for next of kin details
    inlines = [NextOfKinInline]

    # Custom fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'national_id', 'address')}),
        ('Profile', {'fields': ('get_profile_picture', 'profile_picture')}),
        ('Account Info', {'fields': ('account_number', 'accounts', 'is_approved')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'national_id', 'password1', 'password2'),
        }),
    )

    actions = ['approve_members', 'disapprove_members', 'export_members']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    get_full_name.short_description = 'Full Name'

    def approval_status(self, obj):
        if obj.is_approved:
            return format_html('<span style="color: green;">✓ Approved</span>')
        else:
            return format_html('<span style="color: orange;">⏳ Pending</span>')
    approval_status.short_description = 'Status'

    def account_balance(self, obj):
        account = obj.accounts.first()
        if account:
            return f"${account.balance}"
        return "-"
    account_balance.short_description = 'Balance'

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="100" height="100" style="border-radius: 50%;" />')
        return "No image"
    get_profile_picture.short_description = 'Current Picture'

    def approve_members(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} members were successfully approved.')
    approve_members.short_description = "Approve selected members"

    def disapprove_members(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} members were disapproved.')
    disapprove_members.short_description = "Disapprove selected members"

@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = ('name', 'member', 'relationship', 'phone_number', 'district')
    list_filter = ('relationship', 'district')
    search_fields = ('name', 'member__username', 'phone_number')
    raw_id_fields = ('member',)
