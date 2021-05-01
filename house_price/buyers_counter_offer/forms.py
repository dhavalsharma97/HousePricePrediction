from django import forms
from .models import BuyersCounterOffer

class BuyersCounterOfferForm(forms.Form):
    CONTRACT_TYPES = (
        ("Purchase Agreement", "Purchase Agreement"),
        ("Counter Offer", "Counter Offer"),
        ("Other", "Other")
    )

    contract_sign_date = forms.DateField(required=False, label="Contract Sign Date")
    contract_offer = forms.ChoiceField(widget=forms.RadioSelect, choices=CONTRACT_TYPES, required=False)
    counter_offer = forms.IntegerField(required=False, label="Counter Offer Number")
    other_contract_offer = forms.CharField(required=False, label="Other Contract Offer")
    property_address = forms.CharField(required=False, label="Property Address")
    buyers_name = forms.CharField(required=False, label="Buyer's Name")
    sellers_name = forms.CharField(required=False, label="Seller's Name")
    counter_offer_accept = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Counter Offer Acceptance")


class BuyersCounterOfferForm1(forms.Form):
    MERIDIAN_TYPES = (
        ("AM", "AM"),
        ("PM", "PM")
    )
    
    other_terms_text_1 = forms.CharField(required=False, label="Other Terms Text")
    other_terms_text_2 = forms.CharField(required=False, label="Other Terms Text")
    other_terms_text_3 = forms.CharField(required=False, label="Other Terms Text")
    other_terms_text_4 = forms.CharField(required=False, label="Other Terms Text")
    other_terms = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Other Terms")
    additional_terms = forms.CharField(required=False, label="Additional Terms Text")
    expiration_time = forms.IntegerField(required=False, label="Expiration Time")
    expiration_meridian = forms.ChoiceField(widget=forms.RadioSelect, choices=MERIDIAN_TYPES, required=False)
    expiration_date = forms.DateField(required=False, label="Expiration Date")