from django.contrib import admin
from .models import BuyersCounterOffer

@admin.register(BuyersCounterOffer)
class BuyersCounterOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyers_name', 'sellers_name')
    
    fieldsets = (
        ('Buyer Details', {
            'fields': ('contract_sign_date', 'contract_offer', 'counter_offer', 'other_contract_offer', 'property_address', 'buyers_name', 'sellers_name', 'envelope_id', 'envelope_id_1', 'sellers_id')
        }),
        ('Offer Details', {
            'fields': ('counter_offer_accept', 'other_terms_text_1', 'other_terms_text_2', 'other_terms_text_3', 'other_terms_text_4', 'other_terms', 'additional_terms')
        }),
        ('Offer Expiration Details', {
            'fields': ('expiration_time', 'expiration_meridian', 'expiration_date')
        })
    )