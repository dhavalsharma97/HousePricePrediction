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
    
    escrow_date = forms.DateField(label="Escrow Date")
    escrow_days = forms.IntegerField(label="Escrow Days")

    apartment = forms.CharField(max_length=50, label="Apartment")
    street = forms.CharField(max_length=50, label="Street")
    city = forms.CharField(max_length=50, label="City")
    county = forms.CharField(max_length=50, label="County")
    zipcode = forms.IntegerField(label="Zipcode")
    parcel_number = forms.CharField(max_length=50, label="Parcel Number")