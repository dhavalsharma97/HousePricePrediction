from django.contrib import admin
from .models import Payment, Property, Buyer, Seller, BuyerAgent, SellerAgent

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_type', 'down_payment')
    list_filter = ['payment_type']

@admin.register(BuyerAgent)
class BuyerAgentAdmin(admin.ModelAdmin):
    list_display = ('brokerage_firm', 'brokerage_license_number', 'agent_name', 'agent_license_number')

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'offer_price')
    fieldsets = (
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Offer Details', {
            'fields': ('offer_price', 'payment')
        }),
        ('Escrow Dose Date', {
            'fields': ('escrow_date', 'escrow_days')
        }),
        ('Agent Details', {
            'fields': ('ad', 'agent', 'agent_firm', 'dual_brokerage', 'prbs')
        })
    )

@admin.register(SellerAgent)
class SellerAgentAdmin(admin.ModelAdmin):
    list_display = ('brokerage_firm', 'brokerage_license_number', 'agent_name', 'agent_license_number')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['agent']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'street', 'city', 'county', 'parcel_number')
    list_filter = ['city', 'county']
    fields = [('apartment', 'street'), ('city', 'county'), ('buyer', 'seller')]