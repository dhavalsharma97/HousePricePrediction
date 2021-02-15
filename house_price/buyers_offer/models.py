from django.db import models
from django.urls import reverse

class BuyersOffer(models.Model):
    """Model representing a Buyer's Offer"""
    
    PAYMENT_TYPES = (
        ("Cash", "Cash"),
        ("Loan", "Loan")
    )

    FUND_VERIFICATION_TYPES = (
        ("Attached with this agreement", "Attached with this agreement"),
        ("3 or more days", "3 or more days")
    )

    DEPOSIT_PAYMENT_TYPES = (
        ("Cashier's Check", "Cashier's Check"),
        ("Personal Check", "Personal Check"),
        ("Other", "Other")
    )

    DEPOSIT_DUE_TYPES = (
        ("Business days after acceptance", "Business days after acceptance"),
        ("Other", "Other")
    )

    LOAN_TYPES = (
        ("Conventional Loan", "Conventional Loan"),
        ("FHA", "FHA"),
        ("VA", "VA"),
        ("Seller Financing", "Seller Financing"),
        ("AFA", "AFA"),
        ("Other", "Other")
    )

    first_name = models.CharField(max_length=100, help_text="Enter the first name")
    last_name = models.CharField(max_length=100, help_text="Enter the last name")
    email = models.EmailField(help_text="Enter the email address")
    phone = models.IntegerField(help_text="Enter the phone number")

    offer_price = models.IntegerField(help_text="Enter the offer price")
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES, help_text="Enter a type of payment")
    
    fund_verification = models.CharField(max_length=50, choices=FUND_VERIFICATION_TYPES, null=True, help_text="Enter the days needed for fund verification")
    fund_verification_other = models.CharField(max_length=50, null=True, help_text="Enter additional details for fund verification")
    
    first_loan_amount = models.IntegerField(null=True, help_text="Enter the first loan amount")
    first_loan_type = models.CharField(max_length=50, choices=LOAN_TYPES, default="Conventional Loan", null=True, help_text="Enter the type of first loan")
    first_loan_type_other = models.CharField(max_length=50, null=True, help_text="Enter additional details for loan type")
    first_loan_fixed_rate = models.IntegerField(null=True, help_text="Enter the fixed loan rate")
    first_loan_adjustable_loan_rate = models.IntegerField(null=True, help_text="Enter the adjustable loan rate")
    first_loan_max_points = models.IntegerField(null=True, help_text="Enter the maximum points to pay")
    down_payment = models.IntegerField(null=True, help_text="Enter the amount of down payment for the loan")
    down_payment_days = models.IntegerField(null=True, help_text="Enter the amount of down payment days for the loan")
    
    second_loan = models.BooleanField(null=True, help_text="Does the buyer have a second loan")
    second_loan_amount = models.IntegerField(null=True, help_text="Enter the first loan amount")
    second_loan_type = models.CharField(max_length=50, choices=LOAN_TYPES, default="Conventional Loan", null=True, help_text="Enter the type of first loan")
    second_loan_type_other = models.CharField(max_length=50, null=True, help_text="Enter additional details for loan type")
    second_loan_fixed_rate = models.IntegerField(null=True, help_text="Enter the fixed loan rate")
    second_loan_adjustable_loan_rate = models.IntegerField(null=True, help_text="Enter the adjustable loan rate")
    second_loan_max_points = models.IntegerField(null=True, help_text="Enter the maximum points to pay")

    appraisal_contingency = models.BooleanField(null=True, help_text="Does the buyer have an appraisal contingency?")
    appraisal_contingency_days = models.IntegerField(null=True, help_text="Enter the appraisal contingency removal days")
    loan_prequalification_days = models.IntegerField(null=True, help_text="Enter the loan prequalification days")
    loan_contingency = models.BooleanField(null=True, help_text="Does the buyer have a loan contingency?")
    loan_contingency_days = models.IntegerField(null=True, help_text="Enter the loan contingency removal days")

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

    initial_deposit = models.IntegerField(null=True, help_text="Enter the initial deposit")
    deposit_payment_type = models.CharField(max_length=50, choices=DEPOSIT_PAYMENT_TYPES, null=True, help_text="Enter the type of deposit payment")
    deposit_payment_type_other = models.CharField(max_length=100, null=True, help_text="Enter the other deposit payment type")
    deposit_due = models.CharField(max_length=50, choices=DEPOSIT_DUE_TYPES, null=True, help_text="Enter the type of deposit due")
    deposit_due_other = models.CharField(max_length=100, null=True, help_text="Enter the other deposit due")
    
    additional_terms = models.CharField(max_length=100, null=True, help_text="Enter the additional financing terms")

    agreement_contingency = models.BooleanField(null=True, help_text="Is this agreement contingent upon sale of any property owned by the buyer?")
    other_terms = models.CharField(max_length=100, null=True, help_text="Enter the other terms")

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        """String for representing the model object"""
        return self.first_name + self.last_name