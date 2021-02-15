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
            'fields': ('offer_price', 'payment_type')
        }),
        ('Cash Payment Details', {
            'fields': ('fund_verification', 'fund_verification_other')
        }),
        ('First Loan Details', {
            'fields': ('first_loan_amount', 'first_loan_type', 'first_loan_type_other', 'first_loan_fixed_rate', 'first_loan_adjustable_loan_rate', 'first_loan_max_points', 'down_payment', 'down_payment_days')
        }),
        ('Second Loan Details', {
            'fields': ('second_loan', 'second_loan_amount', 'second_loan_type', 'second_loan_type_other', 'second_loan_fixed_rate', 'second_loan_adjustable_loan_rate', 'second_loan_max_points')
        }),
        ('Contingency Details', {
            'fields': ('appraisal_contingency', 'appraisal_contingency_days', 'loan_prequalification_days', 'loan_contingency', 'loan_contingency_days')
        }),
        ('Property Details', {
            'fields': ('apartment', 'street', 'city', 'county', 'zipcode', 'parcel_number')
        }),
        ('Escrow Dose Date', {
            'fields': ('escrow_date', 'escrow_days')
        }),
        ('Agent Details', {
            'fields': ('ad', 'buyer_agent', 'dual_brokerage', 'seller_agent', 'prbs')
        }),
        ('Deposit Details', {
            'fields': ('initial_deposit', 'deposit_payment_type', 'deposit_payment_type_other', 'deposit_due', 'deposit_due_other', 'additional_terms')
        }),
        ('Sale Details', {
            'fields': ('agreement_contingency', 'other_terms')
        })
    )

    list_filter = ['apartment', 'street']