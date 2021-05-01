from django.db import models

class BuyersCounterOffer(models.Model):
    """Model representing a Buyer's Counter Offer"""

    # Radio Button Types
    CONTRACT_TYPES = (
        ("Purchase Agreement", "Purchase Agreement"),
        ("Counter Offer", "Counter Offer"),
        ("Other", "Other")
    )

    MERIDIAN_TYPES = (
        ("AM", "AM"),
        ("PM", "PM")
    )

    # Buyer Details
    contract_sign_date = models.DateField(null=True, help_text="Enter the Contract Sign Date")
    contract_offer = models.CharField(max_length=50, choices=CONTRACT_TYPES, null=True, help_text="Enter the contract offer for the counter offer")
    counter_offer = models.IntegerField(null=True, help_text="Enter the buyers counter offer number")
    other_contract_offer = models.CharField(max_length=100, null=True, help_text="Enter the other contract offer")
    property_address = models.CharField(max_length=100, null=True, help_text="Enter the property address")
    buyers_name = models.CharField(max_length=100, null=True, help_text="Enter the buyer's name")
    sellers_name = models.CharField(max_length=100, null=True, help_text="Enter the seller's name")
    envelope_id = models.CharField(max_length=100, null=True, help_text="Enter the Envelope ID")
    envelope_id_1 = models.CharField(max_length=100, null=True, help_text="Enter the Envelope ID")
    sellers_id = models.IntegerField(null=True, help_text="Enter the seller's ID")

    # Offer Details
    counter_offer_accept = models.BooleanField(null=True, help_text="Does the buyer want to accept the offer?")
    other_terms_text_1 = models.CharField(max_length=100, null=True, help_text="Enter the other terms")
    other_terms_text_2 = models.CharField(max_length=100, null=True, help_text="Enter the other terms")
    other_terms_text_3 = models.CharField(max_length=100, null=True, help_text="Enter the other terms")
    other_terms_text_4 = models.CharField(max_length=100, null=True, help_text="Enter the other terms")
    other_terms = models.BooleanField(null=True, help_text="Does the buyer have any other terms?")
    additional_terms = models.CharField(max_length=100, null=True, help_text="Enter the additional terms")

    # Offer Expiration Details
    expiration_time = models.IntegerField(null=True, help_text="Enter the expiration time")
    expiration_meridian = models.CharField(max_length=50, choices=MERIDIAN_TYPES, null=True, help_text="Enter the expiration meridian")
    expiration_date = models.DateField(null=True, help_text="Enter the expiration date")