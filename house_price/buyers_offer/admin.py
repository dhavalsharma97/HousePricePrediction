from django.contrib import admin
from .models import BuyersOffer

@admin.register(BuyersOffer)
class BuyersOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'apartment', 'street')
    
    fieldsets = (
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Offer Details', {
            'fields': ('offer_price', 'payment_type', 'down_payment')
        }),
        ('Property Details', {
            'fields': ('apartment', 'street', 'city', 'county', 'zipcode', 'parcel_number')
        }),
        ('Escrow Dose Date', {
            'fields': ('escrow_date', 'escrow_days')
        }),
        ('Agent Details', {
            'fields': ('ad', 'buyer_agent', 'dual_brokerage', 'seller_agent', 'prbs')
        })
    )

    list_filter = ['apartment', 'street']