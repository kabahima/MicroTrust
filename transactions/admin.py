from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import Deposit, Withdrawal, Shares

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date', 'description', 'created_at')
    list_filter = ('date', 'created_at', 'account__account_type')
    search_fields = ('account__name', 'account__account_number', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('account', 'amount', 'description')
        }),
        ('Timestamps', {
            'fields': ('date', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('account')

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date', 'description', 'created_at')
    list_filter = ('date', 'created_at', 'account__account_type')
    search_fields = ('account__name', 'account__account_number', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('account', 'amount', 'description')
        }),
        ('Timestamps', {
            'fields': ('date', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('account')

@admin.register(Shares)
class SharesAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'share_count', 'date_purchased', 'created_at')
    list_filter = ('date_purchased', 'created_at')
    search_fields = ('member__username', 'member__first_name', 'member__last_name')
    readonly_fields = ('created_at', 'share_count')
    date_hierarchy = 'date_purchased'
    
    fieldsets = (
        ('Share Purchase Details', {
            'fields': ('member', 'amount', 'share_count')
        }),
        ('Timestamps', {
            'fields': ('date_purchased', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def share_count(self, obj):
        return int(obj.amount)  # Assuming $1 per share
    share_count.short_description = 'Number of Shares'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('member')

# Custom admin site configuration
admin.site.site_header = "MicroTrust Administration"
admin.site.site_title = "MicroTrust Admin"
admin.site.index_title = "Welcome to MicroTrust Administration"
