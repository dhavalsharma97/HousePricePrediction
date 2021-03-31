from django.contrib import admin
from .models import SellersCounterOffer

@admin.register(SellersCounterOffer)
class SellersCounterOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyers_name', 'sellers_name')
    
    fieldsets = (
        ('Seller Details', {
            'fields': ('contract_sign_date', 'multiple_offers', 'contract_offer', 'counter_offer', 'other_contract_offer', 'property_address', 'buyers_name', 'sellers_name', 'sellers_spouse_name', 'sellers_email', 'sellers_spouse_email', 'envelope_id', 'envelope_id_1', 'buyers_id')
        }),
        ('Offer Details', {
            'fields': ('offer_price_change', 'new_offer_price', 'escrow_company_change', 'escrow_company_name', 'title_company_change', 'title_company_name', 'termite_company_change', 'termite_company_name', 'other_terms', 'other_terms_text', 'remove_appraisal_contingence', 'remove_inspection_contingence', 'loan_qualification_proofs', 'addenda', 'addenda_name_1', 'addenda_name_2', 'addenda_name_3')
        }),
        ('Offer Expiration Details', {
            'fields': ('expiration_time', 'expiration_meridian', 'expiration_date')
        })
    )