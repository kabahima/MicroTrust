from django.contrib import admin
from django.utils.html import format_html
from .models import AccountType, Account

@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'account_count')
    search_fields = ('name', 'description')
    
    def account_count(self, obj):
        return obj.accounts.count()
    account_count.short_description = 'Number of Accounts'

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'name', 'account_type', 'balance', 'shares_balance', 'member_count', 'created_at')
    list_filter = ('account_type', 'created_at')
    search_fields = ('account_number', 'name')
    readonly_fields = ('account_number', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Account Information', {
            'fields': ('account_number', 'name', 'description', 'account_type')
        }),
        ('Balances', {
            'fields': ('balance', 'shares_balance'),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def member_count(self, obj):
        count = obj.members.count()
        if count > 0:
            return format_html('<span style="color: green;">{} members</span>', count)
        return format_html('<span style="color: red;">No members</span>')
    member_count.short_description = 'Members'
