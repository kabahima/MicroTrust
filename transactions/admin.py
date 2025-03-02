from django.contrib import admin
from .models import Deposit, Withdrawal, Shares

class DepositAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date', 'description')
    search_fields = ('account__member__username',)

class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date', 'description')
    search_fields = ('account__member__username',)

class SharesAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date_purchased')
    search_fields = ('member__username',)

admin.site.register(Deposit, DepositAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)
admin.site.register(Shares, SharesAdmin)
