from django.contrib import admin
from .models import CustomUser, BuyersOffer
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets, 
        (
            'User ID',
            {
                'fields': [
                    'primary_key'
                ]
            }
        )
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(BuyersOffer)
class BuyersOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'apartment', 'street')
    
    fieldsets = (
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'spouse_first_name', 'spouse_last_name', 'spouse_email')
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
            'fields': ('ad', 'buyer_agent', 'buyer_brokerage_firm', 'buyer_brokerage_license_number', 'buyer_agent_name', 'buyer_agent_license_number', 'dual_brokerage', 'seller_agent', 'seller_brokerage_firm', 'seller_brokerage_license_number', 'seller_agent_name', 'seller_agent_license_number', 'prbs')
        }),
        ('Deposit Details', {
            'fields': ('initial_deposit', 'deposit_payment_type', 'deposit_payment_type_other', 'deposit_due', 'deposit_due_other', 'additional_terms')
        }),
        ('Sale Details', {
            'fields': ('agreement_contingency', 'other_terms')
        }),
        ('Cost Allocation Details', {
            'fields': ('natural_hazard', 'tax_report', 'environmental_report', 'insurance_claim_report', 'termite_inspection_report', 'smoke_alarm', 'government_inspection', 'government_retrofit', 'escrow_fee', 'escrow_holder', 'escrow_general_provision', 'title_insurance', 'title_policy', 'county_transfer', 'city_transfer', 'hoa_transfer', 'hoa_document', 'private_transfer', 'section_1_termite', 'tc_fee', 'warranty_waive', 'warranty_plan', 'warranty_maximal_cost', 'upgraded_warranty', 'warranty_company', 'warranty_air_conditioner', 'warranty_pool_spa', 'warranty_buyers_choice')
        }),
        ('Item Details', {
            'fields': ('stove', 'exceptions_1', 'refrigerators', 'exceptions_2', 'dryers_washers', 'exceptions_3', 'additional_items', 'phone_automation_system', 'not_owned_seller')
        }),
        ('Closing and Possession Details', {
            'fields': ('buyer_primary_residence', 'buyer_possession_1', 'buyer_possession_2', 'buyer_possession_3', 'property_vacant_1', 'property_vacant_2')
        }),
        ('Statutory and Disclosure Details', {
            'fields': ['condominium']
        }),
        ('Time Period Details', {
            'fields': ('deliver_report', 'inspection_contingency', 'remove_inspection_contingency', 'property_access', 'days_perform', 'cancel_agreement')
        }),
        ('Verification Details', {
            'fields': ['final_verification']
        }),
        ('Expiration of Offer Details', {
            'fields': ('expiration_date', 'expiration_time')
        }),
        ('Envelope Details', {
            'fields': ['envelope_id']
        })
    )

    list_filter = ['apartment', 'street']