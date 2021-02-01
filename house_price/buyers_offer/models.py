from django.db import models
from django.urls import reverse
import uuid


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


class PropertyAddress(models.Model):
    """Model representing a payment type"""
    apartment = models.CharField(max_length=50, help_text="Enter the property apartment")
    street = models.CharField(max_length=50, help_text="Enter the property street")
    city = models.CharField(max_length=50, help_text="Enter a type of property city")
    county = models.CharField(max_length=50, help_text="Enter a type of property county")
    zipcode = models.IntegerField(help_text="Enter a type of property zipcode")

    def __str__(self):
        """String for representing the model object"""
        return self.apartment


class Buyer(models.Model):
    """Model representing a Buyer"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular buyer')
    first_name = models.CharField(max_length=100, help_text="Enter the first name")
    last_name = models.CharField(max_length=100, help_text="Enter the last name")
    email = models.EmailField(help_text="Enter the email address")
    phone = models.IntegerField(help_text="Enter the phone number")
    offer_price = models.IntegerField(help_text="Enter the offer price")
    property_address = models.ManyToManyField(PropertyAddress, help_text="Enter the address of property")
    payment = models.ManyToManyField(Payment, help_text="Enter the payment")

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        """String for representing the Model object"""
        return self.first_name