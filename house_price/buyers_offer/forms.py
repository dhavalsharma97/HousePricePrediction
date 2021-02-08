from django import forms

class BuyersOfferForm(forms.Form):
    offer_price = forms.IntegerField(min_value=0)

    CHOICES = [
        ('Cash', 'Cash'),
        ('Loan', 'Loan')
        ]
    payment_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    down_payment = forms.IntegerField(min_value=-1, initial=-1)

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