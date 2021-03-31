from django.db import models

class SellersCounterOffer(models.Model):
    """Model representing a Seller's Counter Offer"""

    # Radio Button Types
    CONTRACT_TYPES = (
        ("Purchase Agreement", "Purchase Agreement"),
        ("Counter Offer", "Counter Offer"),
        ("Other", "Other")
    )

    OFFER_PRICE_TYPES = (
        ("Default", "Default"),
        ("Highest And Best Price", "Highest And Best Price")
    )

    MERIDIAN_TYPES = (
        ("AM", "AM"),
        ("PM", "PM")
    )

    # Seller Details
    contract_sign_date = models.DateField(null=True, help_text="Enter the Contract Sign Date")
    multiple_offers = models.BooleanField(null=True, help_text="Does the seller have multiple offers?")
    contract_offer = models.CharField(max_length=50, choices=CONTRACT_TYPES, null=True, help_text="Enter the contract offer for the counter offer")
    counter_offer = models.IntegerField(null=True, help_text="Enter the buyers counter offer number")
    other_contract_offer = models.CharField(max_length=100, null=True, help_text="Enter the other contract offer")
    property_address = models.CharField(max_length=100, null=True, help_text="Enter the property address")
    buyers_name = models.CharField(max_length=100, null=True, help_text="Enter the buyer's name")
    sellers_name = models.CharField(max_length=100, null=True, help_text="Enter the seller's name")
    sellers_spouse_name = models.CharField(max_length=100, null=True, help_text="Enter the seller's spouse's name")
    sellers_email = models.CharField(max_length=100, null=True, help_text="Enter the seller's email")
    sellers_spouse_email = models.CharField(max_length=100, null=True, help_text="Enter the seller's spouse's email")
    envelope_id = models.CharField(max_length=100, null=True, help_text="Enter the Envelope ID")
    envelope_id_1 = models.CharField(max_length=100, null=True, help_text="Enter the Envelope ID")
    buyers_id = models.IntegerField(null=True, help_text="Enter the buyer's ID")

    # Offer Details
    offer_price_change = models.BooleanField(null=True, help_text="Does the seller want to change the offer price?")
    new_offer_price = models.CharField(max_length=50, choices=OFFER_PRICE_TYPES, null=True, help_text="Enter the new price")
    escrow_company_change = models.BooleanField(null=True, help_text="Does the seller want to change the escrow company?")
    escrow_company_name = models.CharField(max_length=100, null=True, help_text="Enter the escrow company name")
    title_company_change = models.BooleanField(null=True, help_text="Does the seller want to change the title company?")
    title_company_name = models.CharField(max_length=100, null=True, help_text="Enter the title company name")
    termite_company_change = models.BooleanField(null=True, help_text="Does the seller want to change the termite company?")
    termite_company_name = models.CharField(max_length=100, null=True, help_text="Enter the termite company name")
    other_terms = models.BooleanField(null=True, help_text="Does the seller have any other terms?")
    other_terms_text = models.CharField(max_length=100, null=True, help_text="Enter the additional terms")
    remove_appraisal_contingence = models.BooleanField(null=True, help_text="Does the seller want to remove appraisal contingence?")
    remove_inspection_contingence = models.BooleanField(null=True, help_text="Does the seller want to remove inspection contingence?")
    loan_qualification_proofs = models.BooleanField(null=True, help_text="Does the seller want buyer to provide loan qualification prrofs?")
    addenda = models.BooleanField(null=True, help_text="Does the seller have any addenda?")
    addenda_name_1 = models.BooleanField(null=True, help_text="Does the seller have any addenda's number?")
    addenda_name_2 = models.CharField(max_length=100, null=True, help_text="Enter the addenda text")
    addenda_name_3 = models.CharField(max_length=100, null=True, help_text="Enter the addenda text")

    # Offer Expiration Details
    expiration_time = models.IntegerField(null=True, help_text="Enter the expiration time")
    expiration_meridian = models.CharField(max_length=50, choices=MERIDIAN_TYPES, null=True, help_text="Enter the expiration meridian")
    expiration_date = models.DateField(null=True, help_text="Enter the expiration date")