from django.db import models
from django.urls import reverse


class Payment(models.Model):
    """Model representing a payment type"""
    PAYMENT_TYPES = (
        ('Cash', 'Cash'),
        ('Loan', 'Loan')
    )

    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES, help_text="Enter a type of payment")
    down_payment = models.IntegerField(help_text="Enter the amount of down payment for the loan")

    def __str__(self):
        """String for representing the model object"""
        return f'{self.payment_type}, {self.down_payment}'


class BuyerAgent(models.Model):
    """Model representing a Buyer's Agent"""
    brokerage_firm = models.CharField(max_length=100, null=True, help_text="Enter the buyer's brokerage firm")
    brokerage_license_number = models.CharField(max_length=100, null=True, help_text="Enter the buyer's brokerage license number")
    agent_name = models.CharField(max_length=100, null=True, help_text="Enter the buyer's agent name")
    agent_license_number = models.CharField(max_length=100, null=True, help_text="Enter the buyer's agent license number")

    def __str__(self):
        """String for representing the model object"""
        return self.agent_name


class Buyer(models.Model):
    """Model representing a Buyer"""
    first_name = models.CharField(max_length=100, help_text="Enter the first name")
    last_name = models.CharField(max_length=100, help_text="Enter the last name")
    email = models.EmailField(help_text="Enter the email address")
    phone = models.IntegerField(help_text="Enter the phone number")
    offer_price = models.IntegerField(help_text="Enter the offer price")
    payment = models.ManyToManyField(Payment, help_text="Enter the payment")
    escrow_date = models.DateField(null=True, help_text="Enter the Escrow Dose Date")
    escrow_days = models.IntegerField(null=True, help_text="Enter the Escrow Dose Days")
    ad = models.BooleanField(null=True, help_text="Enter the acknowledgement of form AD")
    agent = models.BooleanField(null=True, help_text="Does the buyer have an agent?")
    agent_firm = models.ManyToManyField(BuyerAgent, help_text="Enter the buyer's agent")
    dual_brokerage = models.BooleanField(null=True, help_text="Is the brokerage dual?")
    prbs = models.BooleanField(null=True, help_text="Enter the acknowledgement of form PRBS")

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        """String for representing the model object"""
        return self.first_name


class SellerAgent(models.Model):
    """Model representing a Seller's Agent"""
    brokerage_firm = models.CharField(max_length=100, null=True, help_text="Enter the seller's brokerage firm")
    brokerage_license_number = models.CharField(max_length=100, null=True, help_text="Enter the seller's brokerage license number")
    agent_name = models.CharField(max_length=100, null=True, help_text="Enter the seller's agent name")
    agent_license_number = models.CharField(max_length=100, null=True, help_text="Enter the seller's agent license number")

    def __str__(self):
        """String for representing the model object"""
        return self.agent_name


class Seller(models.Model):
    """Model representing a Seller"""
    agent = models.BooleanField(null=True, help_text="Does the seller have an agent?")
    agent_firm = models.ManyToManyField(SellerAgent, help_text="Enter the seller's agent")

    def __str__(self):
        """String for representing the model object"""
        return 'True'


class Property(models.Model):
    """Model representing a payment type"""
    apartment = models.CharField(max_length=50, help_text="Enter the property apartment")
    street = models.CharField(max_length=50, help_text="Enter the property street")
    city = models.CharField(max_length=50, help_text="Enter the property city")
    county = models.CharField(max_length=50, help_text="Enter the property county")
    zipcode = models.IntegerField(help_text="Enter the property zipcode")
    parcel_number = models.CharField(max_length=50, help_text="Enter the parcel number")
    buyer = models.ManyToManyField(Buyer, help_text="Enter the buyer information")
    seller = models.ManyToManyField(Seller, help_text="Enter the seller information")

    def __str__(self):
        """String for representing the model object"""
        return self.apartment + self.street