from django.db import models
from django.urls import reverse

class BuyersOffer(models.Model):
    """Model representing a Buyer's Offer"""
    
    PAYMENT_TYPES = (
        ('Cash', 'Cash'),
        ('Loan', 'Loan')
    )

    first_name = models.CharField(max_length=100, help_text="Enter the first name")
    last_name = models.CharField(max_length=100, help_text="Enter the last name")
    email = models.EmailField(help_text="Enter the email address")
    phone = models.IntegerField(help_text="Enter the phone number")

    offer_price = models.IntegerField(help_text="Enter the offer price")
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES, help_text="Enter a type of payment")
    down_payment = models.IntegerField(help_text="Enter the amount of down payment for the loan")

    apartment = models.CharField(max_length=50, help_text="Enter the property apartment")
    street = models.CharField(max_length=50, help_text="Enter the property street")
    city = models.CharField(max_length=50, help_text="Enter the property city")
    county = models.CharField(max_length=50, help_text="Enter the property county")
    zipcode = models.IntegerField(help_text="Enter the property zipcode")
    parcel_number = models.CharField(max_length=50, help_text="Enter the parcel number")

    escrow_date = models.DateField(null=True, help_text="Enter the Escrow Dose Date")
    escrow_days = models.IntegerField(null=True, help_text="Enter the Escrow Dose Days")

    ad = models.BooleanField(null=True, help_text="Enter the acknowledgement of form AD")
    
    buyer_agent = models.BooleanField(null=True, help_text="Does the buyer have an agent?")
    buyer_brokerage_firm = models.CharField(max_length=100, null=True, help_text="Enter the buyer's brokerage firm")
    buyer_brokerage_license_number = models.CharField(max_length=100, null=True, help_text="Enter the buyer's brokerage license number")
    buyer_agent_name = models.CharField(max_length=100, null=True, help_text="Enter the buyer's agent name")
    buyer_agent_license_number = models.CharField(max_length=100, null=True, help_text="Enter the buyer's agent license number")

    dual_brokerage = models.BooleanField(null=True, help_text="Is the brokerage dual?")

    seller_agent = models.BooleanField(null=True, help_text="Does the seller have an agent?")
    seller_brokerage_firm = models.CharField(max_length=100, null=True, help_text="Enter the seller's brokerage firm")
    seller_brokerage_license_number = models.CharField(max_length=100, null=True, help_text="Enter the seller's brokerage license number")
    seller_agent_name = models.CharField(max_length=100, null=True, help_text="Enter the seller's agent name")
    seller_agent_license_number = models.CharField(max_length=100, null=True, help_text="Enter the seller's agent license number")
    
    prbs = models.BooleanField(null=True, help_text="Enter the acknowledgement of form PRBS")

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        """String for representing the model object"""
        return self.first_name + self.last_name