from django import forms
from .models import SellersCounterOffer

class SellersCounterOfferForm(forms.Form):
    CONTRACT_TYPES = (
        ("Purchase Agreement", "Purchase Agreement"),
        ("Counter Offer", "Counter Offer"),
        ("Other", "Other")
    )

    OFFER_PRICE_TYPES = (
        ("Default", "Default"),
        ("Highest And Best Price", "Highest And Best Price")
    )

    MERIDIAN_TYPES = (
        ("AM", "AM"),
        ("PM", "PM")
    )

    contract_sign_date = forms.DateField(required=False, label="Contract Sign Date")
    multiple_offers = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Multiple Offers")
    contract_offer = forms.ChoiceField(widget=forms.RadioSelect, choices=CONTRACT_TYPES, required=False)
    counter_offer = forms.CharField(required=False, label="Counter Offer Number")
    property_address = forms.CharField(required=False, label="Property Address")
    buyers_name = forms.CharField(required=False, label="Buyer's Name")
    sellers_name = forms.CharField(required=False, label="Seller's Name")
    offer_price_change = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Offer Price Change")
    new_offer_price = forms.ChoiceField(widget=forms.RadioSelect, choices=OFFER_PRICE_TYPES, required=False)
    escrow_company_change = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Escrow Company Change")
    escrow_company_name = forms.CharField(required=False, label="Escrow Company Name")
    title_company_change = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Title Company Change")
    title_company_name = forms.CharField(required=False, label="Title Company Name")
    termite_company_change = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Termite Company Change")
    termite_company_name = forms.CharField(required=False, label="Termite Company Name")
    other_terms = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Other Terms")
    other_terms_text = forms.CharField(required=False, label="Other Terms Text")
    remove_appraisal_contingence = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Remove Appraisal Contingence")
    remove_inspection_contingence = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Remove Inspection Contingence")
    loan_qualification_proofs = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Loan Qualification Proofs")
    addenda = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Addenda")
    addenda_name_1 = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label="Addenda Number")
    addenda_name_2 = forms.CharField(required=False, label="Addenda Text")
    addenda_name_3 = forms.CharField(required=False, label="Addenda Text")
    expiration_time = forms.IntegerField(required=False, label="Expiration Time")
    expiration_meridian = forms.ChoiceField(widget=forms.RadioSelect, choices=MERIDIAN_TYPES, required=False)
    expiration_date = forms.DateField(required=False, label="Expiration Date")