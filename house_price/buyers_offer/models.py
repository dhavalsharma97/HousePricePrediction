from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    primary_key = models.CharField(max_length=200, null=True)
    primary_key_1 = models.CharField(max_length=200, null=True)

class BuyersOffer(models.Model):
    """Model representing a Buyer's Offer"""
    
    # Radio Button Types
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

    COST_ALLOCATION_TYPES = (
        ("Buyer", "Buyer"),
        ("Seller", "Seller")
    )

    COST_ALLOCATION_TYPES_2 = (
        ("Buyer", "Buyer"),
        ("Seller", "Seller"),
        ("Both", "Both")
    )

    # Personal Details
    first_name = models.CharField(max_length=100, help_text="Enter the first name")
    last_name = models.CharField(max_length=100, help_text="Enter the last name")
    email = models.EmailField(help_text="Enter the email address")
    phone = models.IntegerField(help_text="Enter the phone number")
    spouse_first_name = models.CharField(max_length=100, help_text="Enter the spouse first name")
    spouse_last_name = models.CharField(max_length=100, help_text="Enter the spouse last name")
    spouse_email = models.EmailField(help_text="Enter the spouse email address")

    # Offer Details
    offer_price = models.IntegerField(help_text="Enter the offer price")
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES, help_text="Enter a type of payment")
    
    # Cash Payment Details
    fund_verification = models.CharField(max_length=50, choices=FUND_VERIFICATION_TYPES, null=True, help_text="Enter the days needed for fund verification")
    fund_verification_other = models.CharField(max_length=50, null=True, help_text="Enter additional details for fund verification")
    
    # First Loan Details
    first_loan_amount = models.IntegerField(null=True, help_text="Enter the first loan amount")
    first_loan_type = models.CharField(max_length=50, choices=LOAN_TYPES, default="Conventional Loan", null=True, help_text="Enter the type of first loan")
    first_loan_type_other = models.CharField(max_length=50, null=True, help_text="Enter additional details for loan type")
    first_loan_fixed_rate = models.IntegerField(null=True, help_text="Enter the fixed loan rate")
    first_loan_adjustable_loan_rate = models.IntegerField(null=True, help_text="Enter the adjustable loan rate")
    first_loan_max_points = models.IntegerField(null=True, help_text="Enter the maximum points to pay")
    down_payment = models.IntegerField(null=True, help_text="Enter the amount of down payment for the loan")
    down_payment_days = models.IntegerField(null=True, help_text="Enter the amount of down payment days for the loan")
    
    # Second Loan Details
    second_loan = models.BooleanField(null=True, help_text="Does the buyer have a second loan")
    second_loan_amount = models.IntegerField(null=True, help_text="Enter the first loan amount")
    second_loan_type = models.CharField(max_length=50, choices=LOAN_TYPES, default="Conventional Loan", null=True, help_text="Enter the type of first loan")
    second_loan_type_other = models.CharField(max_length=50, null=True, help_text="Enter additional details for loan type")
    second_loan_fixed_rate = models.IntegerField(null=True, help_text="Enter the fixed loan rate")
    second_loan_adjustable_loan_rate = models.IntegerField(null=True, help_text="Enter the adjustable loan rate")
    second_loan_max_points = models.IntegerField(null=True, help_text="Enter the maximum points to pay")

    # Contingency Details
    appraisal_contingency = models.BooleanField(null=True, help_text="Does the buyer have an appraisal contingency?")
    appraisal_contingency_days = models.IntegerField(null=True, help_text="Enter the appraisal contingency removal days")
    loan_prequalification_days = models.IntegerField(null=True, help_text="Enter the loan prequalification days")
    loan_contingency = models.BooleanField(null=True, help_text="Does the buyer have a loan contingency?")
    loan_contingency_days = models.IntegerField(null=True, help_text="Enter the loan contingency removal days")

    # Property Details
    apartment = models.CharField(max_length=50, help_text="Enter the property apartment")
    street = models.CharField(max_length=50, help_text="Enter the property street")
    city = models.CharField(max_length=50, help_text="Enter the property city")
    county = models.CharField(max_length=50, help_text="Enter the property county")
    zipcode = models.IntegerField(help_text="Enter the property zipcode")
    parcel_number = models.CharField(max_length=50, help_text="Enter the parcel number")

    # Escrow Dose Date
    escrow_date = models.DateField(null=True, help_text="Enter the Escrow Dose Date")
    escrow_days = models.IntegerField(null=True, help_text="Enter the Escrow Dose Days")

    # Agent Details
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

    # Deposit Details
    initial_deposit = models.IntegerField(null=True, help_text="Enter the initial deposit")
    deposit_payment_type = models.CharField(max_length=50, choices=DEPOSIT_PAYMENT_TYPES, null=True, help_text="Enter the type of deposit payment")
    deposit_payment_type_other = models.CharField(max_length=100, null=True, help_text="Enter the other deposit payment type")
    deposit_due = models.CharField(max_length=50, choices=DEPOSIT_DUE_TYPES, null=True, help_text="Enter the type of deposit due")
    deposit_due_other = models.CharField(max_length=100, null=True, help_text="Enter the other deposit due")
    additional_terms = models.CharField(max_length=100, null=True, help_text="Enter the additional financing terms")

    # Sale Details
    agreement_contingency = models.BooleanField(null=True, help_text="Is this agreement contingent upon sale of any property owned by the buyer?")
    other_terms = models.CharField(max_length=100, null=True, help_text="Enter the other terms")

    # Cost Allocation Details
    natural_hazard = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, null=True, help_text="Enter the type of cost allocation")
    tax_report = models.BooleanField(null=True, help_text="Is there a tax report?")
    environmental_report = models.BooleanField(null=True, help_text="Is there an environmental report?")
    insurance_claim_report = models.BooleanField(null=True, help_text="Is there an insurance claim report?")
    termite_inspection_report = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, null=True, help_text="Enter the type of cost allocation")
    smoke_alarm = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, null=True, help_text="Enter the type of cost allocation")
    government_inspection = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, null=True, help_text="Enter the type of cost allocation")
    government_retrofit = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, null=True, help_text="Enter the type of cost allocation")
    escrow_fee = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES_2, null=True, help_text="Enter the type of cost allocation")
    escrow_holder = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Seller", null=True, help_text="Enter the type of cost allocation")
    escrow_general_provision = models.IntegerField(null=True, help_text="Enter the escrow holder's general provision")
    title_insurance = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Seller", null=True, help_text="Enter the type of cost allocation")
    title_policy = models.CharField(max_length=100, null=True, help_text="Enter the institute for preparing the owner's title policy")
    county_transfer = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Seller", null=True, help_text="Enter the type of cost allocation")
    city_transfer = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Seller", null=True, help_text="Enter the type of cost allocation")
    hoa_transfer = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Seller", null=True, help_text="Enter the type of cost allocation")
    hoa_document = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Seller", null=True, help_text="Enter the type of cost allocation")
    private_transfer = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Seller", null=True, help_text="Enter the type of cost allocation")
    section_1_termite = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Seller", null=True, help_text="Enter the type of cost allocation")
    tc_fee = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Buyer", null=True, help_text="Enter the type of cost allocation")
    warranty_waive = models.BooleanField(null=True, help_text="Would the buyer waive the warranty?")
    warranty_plan = models.CharField(max_length=50, choices=COST_ALLOCATION_TYPES, default="Seller", null=True, help_text="Enter the type of cost allocation")
    warranty_maximal_cost = models.IntegerField(null=True, help_text="Enter the maximal cost for warranty")
    upgraded_warranty = models.BooleanField(null=True, help_text="Is it an upgraded warranty?")
    warranty_company = models.CharField(max_length=100, null=True, help_text="Enter the warranty company")
    warranty_air_conditioner = models.BooleanField(null=True, help_text="Would the warranty cover air conditioner?")
    warranty_pool_spa = models.BooleanField(null=True, help_text="Would the warranty cover pool/spa?")
    warranty_buyers_choice = models.BooleanField(null=True, help_text="Shall the warranty be up to buyer's choice?")

    # Item Details
    stove = models.BooleanField(null=True, help_text="Would the sale include all the stoves?")
    exceptions_1 = models.CharField(max_length=100, null=True, help_text="Enter the exceptions")
    refrigerators = models.BooleanField(null=True, help_text="Would the sale include all the refrigerators?")
    exceptions_2 = models.CharField(max_length=100, null=True, help_text="Enter the exceptions")
    dryers_washers = models.BooleanField(null=True, help_text="Would the sale include all the dryers and washers?")
    exceptions_3 = models.CharField(max_length=100, null=True, help_text="Enter the exceptions")
    additional_items = models.CharField(max_length=100, null=True, help_text="Enter the additional items")
    phone_automation_system = models.BooleanField(null=True, default=True, help_text="Would the sale include all the refrigerators?")
    not_owned_seller = models.CharField(max_length=100, null=True, help_text="Enter the items not owned by seller")

    # Closing and Possession Details
    buyer_primary_residence = models.BooleanField(null=True, default=True, help_text="Is the property the buyer's primary residence?")
    buyer_possession_1 = models.CharField(max_length=100, null=True, help_text="Enter the time of close of escrow")
    buyer_possession_2 = models.CharField(max_length=100, null=True, help_text="Enter the time of close of escrow")
    buyer_possession_3 = models.CharField(max_length=100, null=True, help_text="Enter the time of close of escrow")
    property_vacant_1 = models.IntegerField(null=True, help_text="Enter the number of days prior to close of escrow to vacant the property")
    property_vacant_2 = models.BooleanField(null=True, help_text="Enter the number of days prior to close of escrow to vacant the property")

    # Statutory and Disclosure Details
    condominium = models.IntegerField(null=True, help_text="Enter the disclosure to buyer if the property is condominium")
    
    # Time Period Details
    deliver_report = models.IntegerField(null=True, help_text="Enter the days after acceptance that seller has to deliver all the reports")
    inspection_contingency = models.BooleanField(null=True, help_text="Enter the buyer's claim inspection contingency")
    remove_inspection_contingency = models.IntegerField(null=True, help_text="Enter the days after acceptance that seller has to deliver all the reports")
    property_access = models.IntegerField(null=True, help_text="Enter the days after acceptance that buyer shall have access to the property")
    days_perform = models.IntegerField(null=True, help_text="Enter the days to perform")
    cancel_agreement = models.IntegerField(null=True, help_text="Enter the days each party shall give the other party while cancelling this agreement")

    # Verification Details
    final_verification = models.IntegerField(null=True, help_text="When to make final verification of condition")

    # Expiration of Offer Details
    expiration_date = models.DateField(null=True, help_text="Enter the expiration date")
    expiration_time = models.CharField(max_length=100, null=True, help_text="Enter the expiration time")

    # Envelope Details
    envelope_id = models.CharField(max_length=100, null=True, help_text="Enter the envelope ID")

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        """String for representing the model object"""
        return self.first_name + self.last_name