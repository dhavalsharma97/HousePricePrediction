from django import forms

class BuyersOfferForm(forms.Form):
    CHOICES = [
        ('Cash', 'Cash'),
        ('Loan', 'Loan')
        ]

    LOAN_TYPES = [
        ("Conventional Loan", "Conventional Loan"),
        ("FHA", "FHA"),
        ("VA", "VA"),
        ("Seller Financing", "Seller Financing"),
        ("AFA", "AFA"),
        ("Other", "Other")
    ]

    FUND_VERIFICATION_TYPES = [
        ("Attached with this agreement", "Attached with this agreement"),
        ("3 or more days", "3 or more days")
    ]

    offer_price = forms.IntegerField(min_value=0)
    payment_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    fund_verification = forms.ChoiceField(widget=forms.RadioSelect, choices=FUND_VERIFICATION_TYPES, required=False)
    fund_verification_other = forms.CharField(required=False, label="Additional Information")
    
    first_loan_amount = forms.IntegerField(initial=0, required=False, label="Loan Amount")
    first_loan_type = forms.ChoiceField(widget=forms.RadioSelect, choices=LOAN_TYPES, initial="Conventional Loan", required=False)
    first_loan_type_other = forms.CharField(required=False, label="Additional Information")
    first_loan_fixed_rate = forms.IntegerField(initial=0, required=False, label="Loan Fixed Rate")
    first_loan_adjustable_loan_rate = forms.IntegerField(initial=0, required=False, label="Adjustable Loan Rate")
    first_loan_max_points = forms.IntegerField(initial=0, required=False, label="Loan Max Points")
    down_payment = forms.IntegerField(initial=0, required=False, label="Down Payment")
    down_payment_days = forms.IntegerField(initial=3, required=False, label="Down Payment Days")
    
    second_loan = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Second Loan")
    second_loan_amount = forms.IntegerField(initial=0, required=False, label="Loan Amount")
    second_loan_type = forms.ChoiceField(widget=forms.RadioSelect, choices=LOAN_TYPES, initial="Conventional Loan", required=False)
    second_loan_type_other = forms.CharField(required=False, label="Additional Information")
    second_loan_fixed_rate = forms.IntegerField(initial=0, required=False, label="Loan Fixed Rate")
    second_loan_adjustable_loan_rate = forms.IntegerField(initial=0, required=False, label="Adjustable Loan Rate")
    second_loan_max_points = forms.IntegerField(initial=0, required=False, label="Loan Max Points")

    appraisal_contingency = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Appraisal Contingency")
    appraisal_contingency_days = forms.IntegerField(initial=17, required=False, label="Appraisal Contingency Days")
    loan_prequalification_days = forms.IntegerField(initial=3, required=False, label="Loan Prequalification Days")
    loan_contingency = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Loan Contingency")
    loan_contingency_days = forms.IntegerField(initial=21, required=False, label="Loan Contingency Days")

    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email Address")
    phone = forms.IntegerField(label="Phone Number")
    
    escrow_date = forms.DateField(required=False, label="Escrow Date")
    escrow_days = forms.IntegerField(required=False, label="Escrow Days")

    apartment = forms.CharField(max_length=50, label="Apartment")
    street = forms.CharField(max_length=50, label="Street")
    city = forms.CharField(max_length=50, label="City")
    county = forms.CharField(max_length=50, label="County")
    zipcode = forms.IntegerField(label="Zipcode")
    parcel_number = forms.CharField(max_length=50, label="Parcel Number")

class BuyersOfferForm1(forms.Form):
    ad = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Acknowledgement of form AD")

    buyer_agent = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Buyer's Agent")
    buyer_brokerage_firm = forms.CharField(max_length=50, required=False, label="Buyer's Brokerage Firm")
    buyer_brokerage_license_number = forms.CharField(max_length=50, required=False, label="Buyer's Brokerage License Number")
    buyer_agent_name = forms.CharField(max_length=50, required=False, label="Buyer's Agent Name")
    buyer_agent_license_number = forms.CharField(max_length=50, required=False, label="Buyer's Agent License Number")
    dual_brokerage = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Dual Brokerage")

    seller_brokerage_firm = forms.CharField(max_length=50, required=False, label="Seller's Brokerage Firm")
    seller_brokerage_license_number = forms.CharField(max_length=50, required=False, label="Seller's Brokerage License Number")
    seller_agent_name = forms.CharField(max_length=50, required=False, label="Seller's Agent Name")
    seller_agent_license_number = forms.CharField(max_length=50, required=False, label="Seller's agent License Number")
    
    prbs = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Acknowledgement of form PRBS")

class BuyersOfferForm2(forms.Form):
    DEPOSIT_PAYMENT_TYPES = [
        ("Cashier's Check", "Cashier's Check"),
        ("Personal Check", "Personal Check"),
        ("Other", "Other")
    ]

    DEPOSIT_DUE_TYPES = [
        ("Business days after acceptance", "Business days after acceptance"),
        ("Other", "Other")
    ]

    initial_deposit = forms.IntegerField(label="Initial Deposit")
    deposit_payment_type = forms.ChoiceField(widget=forms.RadioSelect, choices=DEPOSIT_PAYMENT_TYPES)
    deposit_payment_type_other = forms.CharField(max_length=50, required=False, label="Additional Information")
    deposit_due = forms.ChoiceField(widget=forms.RadioSelect, choices=DEPOSIT_DUE_TYPES, initial="Business days after acceptance")
    deposit_due_other = forms.CharField(max_length=50, required=False, label="Additional Information")
    
    additional_terms = forms.CharField(max_length=50, required=False, label="Additional Terms")
    agreement_contingency = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Agreement Contingency")
    other_terms = forms.CharField(max_length=100, label="Other Terms")

class BuyersOfferForm3(forms.Form):
    COST_ALLOCATION_TYPES = (
        ("Buyer", "Buyer"),
        ("Seller", "Seller")
    )

    COST_ALLOCATION_TYPES_2 = (
        ("Buyer", "Buyer"),
        ("Seller", "Seller"),
        ("Both", "Both")
    )

    natural_hazard = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, required=False)
    tax_report = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Tax Report")
    environmental_report = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Environmental Report")
    insurance_claim_report = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Insurance Claim Report")
    termite_inspection_report = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES)
    smoke_alarm = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES)
    government_inspection = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES)
    government_retrofit = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES)
    escrow_fee = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES_2)
    escrow_holder = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Seller")
    escrow_general_provision = forms.IntegerField(initial=5, label="Initial Deposit")
    title_insurance = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Seller")
    title_policy = forms.CharField(max_length=50, initial="Seller's Choice", label="Additional Information")
    county_transfer = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Seller")
    city_transfer = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Seller")
    hoa_transfer = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Seller")
    hoa_document = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Seller")
    private_transfer = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Seller")
    section_1_termite = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Seller")
    tc_fee = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Buyer")
    warranty_waive = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Waive Warranty")
    warranty_plan = forms.ChoiceField(widget=forms.RadioSelect, choices=COST_ALLOCATION_TYPES, initial="Seller", required=False)
    warranty_maximal_cost = forms.IntegerField(label="Warranty Maximal Cost", required=False)
    upgraded_warranty = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Upgraded Warranty")
    warranty_company = forms.CharField(max_length=50, required=False, label="Warranty Company")
    warranty_air_conditioner = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Air Conditioner Warranty")
    warranty_pool_spa = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Pool/Spa Warranty")
    warranty_buyers_choice = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Buyer's Choice Warranty")