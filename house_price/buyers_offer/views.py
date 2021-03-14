from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
import base64
import docusign_esign
import requests
import apiclient
import shutil
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

from buyers_offer.models import CustomUser, BuyersOffer
from buyers_offer.forms import CustomUserCreationForm, BuyersOfferForm, BuyersOfferForm1, BuyersOfferForm2, BuyersOfferForm3, BuyersOfferForm4
from helpers.helper import fill_pdf

CLIENT_AUTH_ID = '6dfb62a5-2b74-4358-81de-327243a9fe60'
CLIENT_SECRET_KEY = '75c8da9b-d4f0-4c06-a15c-2ab6815edf6b'
CLIENT_ACCOUNT_ID = '13197074'

def index(request):
    """View function for home page of site"""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def offer_form(request):
    """View function for buyers offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersOfferForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # If the record already exists
            if BuyersOffer.objects.filter(pk=user.primary_key).count() > 0:
                buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)
                buyers_offer_obj.first_name=form.cleaned_data['first_name']
                buyers_offer_obj.last_name=form.cleaned_data['last_name']
                buyers_offer_obj.email=form.cleaned_data['email']
                buyers_offer_obj.phone=form.cleaned_data['phone']
                buyers_offer_obj.spouse_first_name=form.cleaned_data['spouse_first_name']
                buyers_offer_obj.spouse_last_name=form.cleaned_data['spouse_last_name']
                buyers_offer_obj.spouse_email=form.cleaned_data['spouse_email']
                buyers_offer_obj.offer_price=form.cleaned_data['offer_price']
                buyers_offer_obj.payment_type=form.cleaned_data['payment_type']
                buyers_offer_obj.apartment=form.cleaned_data['apartment']
                buyers_offer_obj.street=form.cleaned_data['street']
                buyers_offer_obj.city=form.cleaned_data['city']
                buyers_offer_obj.county=form.cleaned_data['county']
                buyers_offer_obj.zipcode=form.cleaned_data['zipcode']
                buyers_offer_obj.parcel_number=form.cleaned_data['parcel_number']
                buyers_offer_obj.escrow_date=form.cleaned_data['escrow_date']
                buyers_offer_obj.escrow_days=form.cleaned_data['escrow_days']
            else:
                # Save the record to database
                buyers_offer_obj = BuyersOffer(first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'],
                                            email=form.cleaned_data['email'],
                                            phone=form.cleaned_data['phone'],
                                            spouse_first_name=form.cleaned_data['spouse_first_name'],
                                            spouse_last_name=form.cleaned_data['spouse_last_name'],
                                            spouse_email=form.cleaned_data['spouse_email'],
                                            offer_price=form.cleaned_data['offer_price'],
                                            payment_type=form.cleaned_data['payment_type'],
                                            apartment=form.cleaned_data['apartment'],
                                            street=form.cleaned_data['street'],
                                            city=form.cleaned_data['city'],
                                            county=form.cleaned_data['county'],
                                            zipcode=form.cleaned_data['zipcode'],
                                            parcel_number=form.cleaned_data['parcel_number'],
                                            escrow_date=form.cleaned_data['escrow_date'],
                                            escrow_days=form.cleaned_data['escrow_days'])
                
                buyers_offer_obj.save()

                # Saving the buyer details
                user.primary_key = buyers_offer_obj.pk
                user.save()

            buyers_offer_obj.fund_verification = form.cleaned_data['fund_verification']
            buyers_offer_obj.fund_verification_other = form.cleaned_data['fund_verification_other']
            buyers_offer_obj.first_loan_amount = form.cleaned_data['first_loan_amount']
            buyers_offer_obj.first_loan_type = form.cleaned_data['first_loan_type']
            buyers_offer_obj.first_loan_type_other = form.cleaned_data['first_loan_type_other']
            buyers_offer_obj.first_loan_fixed_rate = form.cleaned_data['first_loan_fixed_rate']
            buyers_offer_obj.first_loan_adjustable_loan_rate = form.cleaned_data['first_loan_adjustable_loan_rate']
            buyers_offer_obj.first_loan_max_points = form.cleaned_data['first_loan_max_points']
            buyers_offer_obj.down_payment = form.cleaned_data['down_payment']
            buyers_offer_obj.down_payment_days = form.cleaned_data['down_payment_days']
            buyers_offer_obj.second_loan = form.cleaned_data['second_loan']
            buyers_offer_obj.second_loan_amount = form.cleaned_data['second_loan_amount']
            buyers_offer_obj.second_loan_type = form.cleaned_data['second_loan_type']
            buyers_offer_obj.second_loan_type_other = form.cleaned_data['second_loan_type_other']
            buyers_offer_obj.second_loan_fixed_rate = form.cleaned_data['second_loan_fixed_rate']
            buyers_offer_obj.second_loan_adjustable_loan_rate = form.cleaned_data['second_loan_adjustable_loan_rate']
            buyers_offer_obj.second_loan_max_points = form.cleaned_data['second_loan_max_points']
            buyers_offer_obj.appraisal_contingency = form.cleaned_data['appraisal_contingency']
            buyers_offer_obj.appraisal_contingency_days = form.cleaned_data['appraisal_contingency_days']
            buyers_offer_obj.loan_prequalification_days = form.cleaned_data['loan_prequalification_days']
            buyers_offer_obj.loan_contingency = form.cleaned_data['loan_contingency']
            buyers_offer_obj.loan_contingency_days = form.cleaned_data['loan_contingency_days']
            buyers_offer_obj.save()

            # Generate PDF
            fill_pdf('buyers_offer', 'purchase_agreement', user.primary_key)

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('offerformconfirm'))

    # If this is a GET (or any other method) create the default form.
    else:
        if BuyersOffer.objects.filter(pk=user.primary_key).count() > 0:
            buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)
            form = BuyersOfferForm(initial={
                'first_name': buyers_offer_obj.first_name,
                'last_name': buyers_offer_obj.last_name,
                'email': buyers_offer_obj.email,
                'phone': buyers_offer_obj.phone,
                'spouse_first_name': buyers_offer_obj.spouse_first_name,
                'spouse_last_name': buyers_offer_obj.spouse_last_name,
                'spouse_email': buyers_offer_obj.spouse_email,
                'offer_price': buyers_offer_obj.offer_price,
                'payment_type': buyers_offer_obj.payment_type,
                'apartment': buyers_offer_obj.apartment,
                'street': buyers_offer_obj.street,
                'city': buyers_offer_obj.city,
                'county': buyers_offer_obj.county,
                'zipcode': buyers_offer_obj.zipcode,
                'parcel_number': buyers_offer_obj.parcel_number,
                'escrow_date': buyers_offer_obj.escrow_date,
                'escrow_days': buyers_offer_obj.escrow_days,
                'fund_verification': buyers_offer_obj.fund_verification,
                'fund_verification_other': buyers_offer_obj.fund_verification_other,
                'first_loan_amount': buyers_offer_obj.first_loan_amount,
                'first_loan_type': buyers_offer_obj.first_loan_type,
                'first_loan_type_other': buyers_offer_obj.first_loan_type_other,
                'first_loan_fixed_rate': buyers_offer_obj.first_loan_fixed_rate,
                'first_loan_adjustable_loan_rate': buyers_offer_obj.first_loan_adjustable_loan_rate,
                'first_loan_max_points': buyers_offer_obj.first_loan_max_points,
                'down_payment': buyers_offer_obj.down_payment,
                'down_payment_days': buyers_offer_obj.down_payment_days,
                'second_loan': buyers_offer_obj.second_loan,
                'second_loan_amount': buyers_offer_obj.second_loan_amount,
                'second_loan_type': buyers_offer_obj.second_loan_type,
                'second_loan_type_other': buyers_offer_obj.second_loan_type_other,
                'second_loan_fixed_rate': buyers_offer_obj.second_loan_fixed_rate,
                'second_loan_adjustable_loan_rate': buyers_offer_obj.second_loan_adjustable_loan_rate,
                'second_loan_max_points': buyers_offer_obj.second_loan_max_points,
                'appraisal_contingency': buyers_offer_obj.appraisal_contingency,
                'appraisal_contingency_days': buyers_offer_obj.appraisal_contingency_days,
                'loan_prequalification_days': buyers_offer_obj.loan_prequalification_days,
                'loan_contingency': buyers_offer_obj.loan_contingency,
                'loan_contingency_days': buyers_offer_obj.loan_contingency_days
            })
        else:
            form = BuyersOfferForm()

    context = {
        'form': form
    }

    return render(request, 'offer_form.html', context)


@login_required
def offer_form_confirm(request):
    """View function for buyers offer confirmation page of site"""

    user = CustomUser.objects.get(pk=request.user.pk)

    # Render the HTML template offer_form_confirm.html
    return render(request, 'offer_form_confirm.html', {'pdf_path': 'pdf/purchase_agreement_filled_' + str(user.primary_key) +'.pdf'})


@login_required
def offer_form_1(request):
    """View function for buyers offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersOfferForm1(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Save the record to database
            buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)

            buyers_offer_obj.ad = form.cleaned_data['ad']
            buyers_offer_obj.buyer_agent = form.cleaned_data['buyer_agent']
            buyers_offer_obj.dual_brokerage = form.cleaned_data['dual_brokerage']
            buyers_offer_obj.prbs = form.cleaned_data['prbs']
            buyers_offer_obj.buyer_brokerage_firm = form.cleaned_data['buyer_brokerage_firm']
            buyers_offer_obj.buyer_brokerage_license_number = form.cleaned_data['buyer_brokerage_license_number']
            buyers_offer_obj.buyer_agent_name = form.cleaned_data['buyer_agent_name']
            buyers_offer_obj.buyer_agent_license_number = form.cleaned_data['buyer_agent_license_number']
            buyers_offer_obj.seller_agent = not form.cleaned_data['dual_brokerage']
            buyers_offer_obj.seller_brokerage_firm = form.cleaned_data['seller_brokerage_firm']
            buyers_offer_obj.seller_brokerage_license_number=form.cleaned_data['seller_brokerage_license_number']
            buyers_offer_obj.seller_agent_name=form.cleaned_data['seller_agent_name']
            buyers_offer_obj.seller_agent_license_number=form.cleaned_data['seller_agent_license_number']

            buyers_offer_obj.save()

            # Generate PDF
            fill_pdf('buyers_offer', 'purchase_agreement', user.primary_key)

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('offerformconfirm1'))

    # If this is a GET (or any other method) create the default form.
    else:
        if BuyersOffer.objects.filter(pk=user.primary_key).count() > 0:
            buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)
            form = BuyersOfferForm1(initial={
                'ad': buyers_offer_obj.ad,
                'buyer_agent': buyers_offer_obj.buyer_agent,
                'dual_brokerage': buyers_offer_obj.dual_brokerage,
                'prbs': buyers_offer_obj.prbs,
                'buyer_brokerage_firm': buyers_offer_obj.buyer_brokerage_firm,
                'buyer_brokerage_license_number': buyers_offer_obj.buyer_brokerage_license_number,
                'buyer_agent_name': buyers_offer_obj.buyer_agent_name,
                'buyer_agent_license_number': buyers_offer_obj.buyer_agent_license_number,
                'seller_agent': not buyers_offer_obj.dual_brokerage,
                'seller_brokerage_firm': buyers_offer_obj.seller_brokerage_firm,
                'seller_brokerage_license_number': buyers_offer_obj.seller_brokerage_license_number,
                'seller_agent_name': buyers_offer_obj.seller_agent_name,
                'seller_agent_license_number': buyers_offer_obj.seller_agent_license_number
            })
        else:
            form = BuyersOfferForm1()

    context = {
        'form': form
    }

    return render(request, 'offer_form_1.html', context)


@login_required
def offer_form_confirm_1(request):
    """View function for buyers offer confirmation page of site"""

    user = CustomUser.objects.get(pk=request.user.pk)

    # Render the HTML template offer_form_confirm_1.html
    return render(request, 'offer_form_confirm_1.html', {'pdf_path': 'pdf/purchase_agreement_filled_' + str(user.primary_key) +'.pdf'})


@login_required
def offer_form_2(request):
    """View function for buyers offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersOfferForm2(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Save the record to database
            buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)

            buyers_offer_obj.initial_deposit = form.cleaned_data['initial_deposit']
            buyers_offer_obj.deposit_payment_type = form.cleaned_data['deposit_payment_type']
            buyers_offer_obj.deposit_payment_type_other = form.cleaned_data['deposit_payment_type_other']
            buyers_offer_obj.deposit_due = form.cleaned_data['deposit_due']
            buyers_offer_obj.deposit_due_other = form.cleaned_data['deposit_due_other']
            buyers_offer_obj.additional_terms = form.cleaned_data['additional_terms']
            buyers_offer_obj.agreement_contingency = form.cleaned_data['agreement_contingency']
            buyers_offer_obj.other_terms = form.cleaned_data['other_terms']
            buyers_offer_obj.save()

            # Generate PDF
            fill_pdf('buyers_offer', 'purchase_agreement', user.primary_key)

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('offerformconfirm2'))

    # If this is a GET (or any other method) create the default form.
    else:
        if BuyersOffer.objects.filter(pk=user.primary_key).count() > 0:
            buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)
            form = BuyersOfferForm2(initial={
                'initial_deposit': buyers_offer_obj.initial_deposit,
                'deposit_payment_type': buyers_offer_obj.deposit_payment_type,
                'deposit_payment_type_other': buyers_offer_obj.deposit_payment_type_other,
                'deposit_due': buyers_offer_obj.deposit_due,
                'deposit_due_other': buyers_offer_obj.deposit_due_other,
                'additional_terms': buyers_offer_obj.additional_terms,
                'agreement_contingency': buyers_offer_obj.agreement_contingency,
                'other_terms': buyers_offer_obj.other_terms
            })
        else:
            form = BuyersOfferForm2()

    context = {
        'form': form
    }

    return render(request, 'offer_form_2.html', context)


@login_required
def offer_form_confirm_2(request):
    """View function for buyers offer confirmation page of site"""

    user = CustomUser.objects.get(pk=request.user.pk)

    # Render the HTML template offer_form_confirm_2.html
    return render(request, 'offer_form_confirm_2.html', {'pdf_path': 'pdf/purchase_agreement_filled_' + str(user.primary_key) +'.pdf'})


@login_required
def offer_form_3(request):
    """View function for buyers offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersOfferForm3(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Save the record to database
            buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)

            buyers_offer_obj.natural_hazard = form.cleaned_data['natural_hazard']
            buyers_offer_obj.tax_report = form.cleaned_data['tax_report']
            buyers_offer_obj.environmental_report = form.cleaned_data['environmental_report']
            buyers_offer_obj.insurance_claim_report = form.cleaned_data['insurance_claim_report']
            buyers_offer_obj.termite_inspection_report = form.cleaned_data['termite_inspection_report']
            buyers_offer_obj.smoke_alarm = form.cleaned_data['smoke_alarm']
            buyers_offer_obj.government_inspection = form.cleaned_data['government_inspection']
            buyers_offer_obj.government_retrofit = form.cleaned_data['government_retrofit']
            buyers_offer_obj.escrow_fee = form.cleaned_data['escrow_fee']
            buyers_offer_obj.escrow_holder = form.cleaned_data['escrow_holder']
            buyers_offer_obj.escrow_general_provision = form.cleaned_data['escrow_general_provision']
            buyers_offer_obj.title_insurance = form.cleaned_data['title_insurance']
            buyers_offer_obj.title_policy = form.cleaned_data['title_policy']
            buyers_offer_obj.county_transfer = form.cleaned_data['county_transfer']
            buyers_offer_obj.city_transfer = form.cleaned_data['city_transfer']
            buyers_offer_obj.hoa_transfer = form.cleaned_data['hoa_transfer']
            buyers_offer_obj.hoa_document = form.cleaned_data['hoa_document']
            buyers_offer_obj.private_transfer = form.cleaned_data['private_transfer']
            buyers_offer_obj.section_1_termite = form.cleaned_data['section_1_termite']
            buyers_offer_obj.tc_fee = form.cleaned_data['tc_fee']
            buyers_offer_obj.warranty_waive = form.cleaned_data['warranty_waive']
            buyers_offer_obj.warranty_plan = form.cleaned_data['warranty_plan']
            buyers_offer_obj.warranty_maximal_cost = form.cleaned_data['warranty_maximal_cost']
            buyers_offer_obj.upgraded_warranty = form.cleaned_data['upgraded_warranty']
            buyers_offer_obj.warranty_company = form.cleaned_data['warranty_company']
            buyers_offer_obj.warranty_air_conditioner = form.cleaned_data['warranty_air_conditioner']
            buyers_offer_obj.warranty_pool_spa = form.cleaned_data['warranty_pool_spa']
            buyers_offer_obj.warranty_buyers_choice = form.cleaned_data['warranty_buyers_choice']
            buyers_offer_obj.save()

            # Generate PDF
            fill_pdf('buyers_offer', 'purchase_agreement', user.primary_key)

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('offerformconfirm3'))

    # If this is a GET (or any other method) create the default form.
    else:
        if BuyersOffer.objects.filter(pk=user.primary_key).count() > 0:
            buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)
            form = BuyersOfferForm3(initial={
                'natural_hazard': buyers_offer_obj.natural_hazard,
                'tax_report': buyers_offer_obj.tax_report,
                'environmental_report': buyers_offer_obj.environmental_report,
                'insurance_claim_report': buyers_offer_obj.insurance_claim_report,
                'termite_inspection_report': buyers_offer_obj.termite_inspection_report,
                'smoke_alarm': buyers_offer_obj.smoke_alarm,
                'government_inspection': buyers_offer_obj.government_inspection,
                'government_retrofit': buyers_offer_obj.government_retrofit,
                'escrow_fee': buyers_offer_obj.escrow_fee,
                'escrow_holder': buyers_offer_obj.escrow_holder,
                'escrow_general_provision': buyers_offer_obj.escrow_general_provision,
                'title_insurance': buyers_offer_obj.title_insurance,
                'title_policy': buyers_offer_obj.title_policy,
                'county_transfer': buyers_offer_obj.county_transfer,
                'city_transfer': buyers_offer_obj.city_transfer,
                'hoa_transfer': buyers_offer_obj.hoa_transfer,
                'hoa_document': buyers_offer_obj.hoa_document,
                'private_transfer': buyers_offer_obj.private_transfer,
                'section_1_termite': buyers_offer_obj.section_1_termite,
                'tc_fee': buyers_offer_obj.tc_fee,
                'warranty_waive': buyers_offer_obj.warranty_waive,
                'warranty_plan': buyers_offer_obj.warranty_plan,
                'warranty_maximal_cost': buyers_offer_obj.warranty_maximal_cost,
                'upgraded_warranty': buyers_offer_obj.upgraded_warranty,
                'warranty_company': buyers_offer_obj.warranty_company,
                'warranty_air_conditioner': buyers_offer_obj.warranty_air_conditioner,
                'warranty_pool_spa': buyers_offer_obj.warranty_pool_spa,
                'warranty_buyers_choice': buyers_offer_obj.warranty_buyers_choice
            })
        else:
            form = BuyersOfferForm3()

    context = {
        'form': form
    }

    return render(request, 'offer_form_3.html', context)


@login_required
def offer_form_confirm_3(request):
    """View function for buyers offer confirmation page of site"""

    user = CustomUser.objects.get(pk=request.user.pk)

    # Render the HTML template offer_form_confirm_3.html
    return render(request, 'offer_form_confirm_3.html', {'pdf_path': 'pdf/purchase_agreement_filled_' + str(user.primary_key) +'.pdf'})


@login_required
def offer_form_4(request):
    """View function for buyers offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersOfferForm4(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Save the record to database
            buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)

            buyers_offer_obj.stove = form.cleaned_data['stove']
            buyers_offer_obj.exceptions_1 = form.cleaned_data['exceptions_1']
            buyers_offer_obj.refrigerators = form.cleaned_data['refrigerators']
            buyers_offer_obj.exceptions_2 = form.cleaned_data['exceptions_2']
            buyers_offer_obj.dryers_washers = form.cleaned_data['dryers_washers']
            buyers_offer_obj.exceptions_3 = form.cleaned_data['exceptions_3']
            buyers_offer_obj.additional_items = form.cleaned_data['additional_items']
            buyers_offer_obj.phone_automation_system = form.cleaned_data['phone_automation_system']
            buyers_offer_obj.not_owned_seller = form.cleaned_data['not_owned_seller']
            buyers_offer_obj.buyer_primary_residence = form.cleaned_data['buyer_primary_residence']
            buyers_offer_obj.buyer_possession_1 = form.cleaned_data['buyer_possession_1']
            buyers_offer_obj.buyer_possession_2 = form.cleaned_data['buyer_possession_2']
            buyers_offer_obj.buyer_possession_3 = form.cleaned_data['buyer_possession_3']
            buyers_offer_obj.property_vacant_1 = form.cleaned_data['property_vacant_1']
            buyers_offer_obj.property_vacant_2 = form.cleaned_data['property_vacant_2']
            buyers_offer_obj.condominium = form.cleaned_data['condominium']
            buyers_offer_obj.deliver_report = form.cleaned_data['deliver_report']
            buyers_offer_obj.inspection_contingency = form.cleaned_data['inspection_contingency']
            buyers_offer_obj.remove_inspection_contingency = form.cleaned_data['remove_inspection_contingency']
            buyers_offer_obj.property_access = form.cleaned_data['property_access']
            buyers_offer_obj.days_perform = form.cleaned_data['days_perform']
            buyers_offer_obj.cancel_agreement = form.cleaned_data['cancel_agreement']
            buyers_offer_obj.final_verification = form.cleaned_data['final_verification']
            buyers_offer_obj.expiration_date = form.cleaned_data['expiration_date']
            buyers_offer_obj.expiration_time = form.cleaned_data['expiration_time']
            buyers_offer_obj.save()

            # Generate PDF
            fill_pdf('buyers_offer', 'purchase_agreement', user.primary_key)

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('offerformconfirm4'))

    # If this is a GET (or any other method) create the default form.
    else:
        if BuyersOffer.objects.filter(pk=user.primary_key).count() > 0:
            buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)
            form = BuyersOfferForm4(initial={
                'stove': buyers_offer_obj.stove,
                'exceptions_1': buyers_offer_obj.exceptions_1,
                'refrigerators': buyers_offer_obj.refrigerators,
                'exceptions_2': buyers_offer_obj.exceptions_2,
                'dryers_washers': buyers_offer_obj.dryers_washers,
                'exceptions_3': buyers_offer_obj.exceptions_3,
                'additional_items': buyers_offer_obj.additional_items,
                'phone_automation_system': buyers_offer_obj.phone_automation_system,
                'not_owned_seller': buyers_offer_obj.not_owned_seller,
                'buyer_primary_residence': buyers_offer_obj.buyer_primary_residence,
                'buyer_possession_1': buyers_offer_obj.buyer_possession_1,
                'buyer_possession_2': buyers_offer_obj.buyer_possession_2,
                'buyer_possession_3': buyers_offer_obj.buyer_possession_3,
                'property_vacant_1': buyers_offer_obj.property_vacant_1,
                'property_vacant_2': buyers_offer_obj.property_vacant_2,
                'condominium': buyers_offer_obj.condominium,
                'deliver_report': buyers_offer_obj.deliver_report,
                'inspection_contingency': buyers_offer_obj.inspection_contingency,
                'remove_inspection_contingency': buyers_offer_obj.remove_inspection_contingency,
                'property_access': buyers_offer_obj.property_access,
                'days_perform': buyers_offer_obj.days_perform,
                'cancel_agreement': buyers_offer_obj.cancel_agreement,
                'final_verification': buyers_offer_obj.final_verification,
                'expiration_date': buyers_offer_obj.expiration_date,
                'expiration_time': buyers_offer_obj.expiration_time
            })
        else:
            form = BuyersOfferForm4()

    context = {
        'form': form
    }

    return render(request, 'offer_form_4.html', context)


@login_required
def offer_form_confirm_4(request):
    """View function for buyers offer confirmation page of site"""

    user = CustomUser.objects.get(pk=request.user.pk)

    # Render the HTML template offer_form_confirm_4.html
    return render(request, 'offer_form_confirm_4.html', {'pdf_path': 'pdf/purchase_agreement_filled_' + str(user.primary_key) +'.pdf'})


@login_required
def offer_form_navigate(request):
    """View function for buyers offer navigation page of site"""

    # Render the HTML template offer_form_navigate.html
    return render(request, 'offer_form_navigate.html')


@login_required
def get_access_code(request):
    """Helper function for getting the access code for e-signature"""

    base_url = "https://account-d.docusign.com/oauth/auth"
    auth_url = "{0}?response_type=code&scope=signature&client_id={1}&redirect_uri={2}".format(base_url, CLIENT_AUTH_ID, request.build_absolute_uri(reverse('auth_login')))

    return HttpResponseRedirect(auth_url)


@login_required
def auth_login(request):
    """Helper function for authenticating the user for e-signature"""

    base_url = "https://account-d.docusign.com/oauth/token"
    auth_code_string = "{0}:{1}".format(CLIENT_AUTH_ID, CLIENT_SECRET_KEY)
    auth_token = base64.b64encode(auth_code_string.encode())

    req_headers = {"Authorization": "Basic {0}".format(auth_token.decode('utf-8'))}
    post_data = {"grant_type": "authorization_code", "code": request.GET.get('code')}

    r = requests.post(base_url, data=post_data, headers=req_headers)

    response = r.json()

    if not 'error' in response:
        return HttpResponseRedirect("{0}?token={1}".format(reverse('get_signing_url'), response['access_token']))

    return HttpResponse(response['error'])


@login_required
def embedded_signing_ceremony(request):
    """View function for the e-signature request"""

    user = CustomUser.objects.get(pk=request.user.pk)
    buyers_offer_obj = BuyersOffer.objects.get(pk=user.primary_key)
    signer_1_email = buyers_offer_obj.email
    signer_1_name = buyers_offer_obj.first_name
    signer_2_email = buyers_offer_obj.spouse_email
    signer_2_name = buyers_offer_obj.spouse_first_name

    with open(os.path.join(BASE_DIR, 'static/pdf', 'purchase_agreement_filled_' + user.primary_key + '.pdf'), "rb") as file:
        content_bytes = file.read()

    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    document = docusign_esign.Document(
        document_base64 = base64_file_content,
        name = 'Buyers Offer Agreement',
        file_extension = 'pdf',
        document_id = '1'
    )

    signer_1 = docusign_esign.Signer(email = signer_1_email, name = signer_1_name, recipient_id = str(user.primary_key) + '00', routing_order = '1', client_user_id = '1')
    sign_here_tabs_1 = []
    sign_here_locations_1 = {
        '1': [('93', '677')],
        '2': [('93', '689')],
        '3': [('93', '695')],
        '4': [('93', '703')],
        '5': [('93', '699')],
        '6': [('93', '702')],
        '7': [('93', '704')],
        '8': [('93', '699')],
        '13': [('305', '327')]
    }

    for page in sign_here_locations_1.keys():
        for location in range(len(sign_here_locations_1[page])):
            sign_here = docusign_esign.SignHere(document_id = '1', page_number = page, recipient_id = str(user.primary_key) + '00', tab_label = 'Sign Here', x_position = sign_here_locations_1[page][location][0], y_position = sign_here_locations_1[page][location][1])
            sign_here_tabs_1.append(sign_here)

    date_signed_tabs_1 = []
    date_signed_locations_1 = {
        '13': [('380', '350')]
    }

    for page in date_signed_locations_1.keys():
        for location in range(len(date_signed_locations_1[page])):
            date_signed = docusign_esign.DateSigned(document_id = '1', page_number = page, recipient_id = str(user.primary_key) + '00', x_position = date_signed_locations_1[page][location][0], y_position = date_signed_locations_1[page][location][1])
            date_signed_tabs_1.append(date_signed)

    signer_2 = docusign_esign.Signer(email = signer_2_email, name = signer_2_name, recipient_id = str(user.primary_key) + '01', routing_order = '1', client_user_id = '1')
    sign_here_tabs_2 = []
    sign_here_locations_2 = {
        '1': [('152', '677')],
        '2': [('152', '689')],
        '3': [('152', '695')],
        '4': [('152', '703')],
        '5': [('152', '699')],
        '6': [('152', '702')],
        '7': [('152', '704')],
        '8': [('152', '699')],
        '13': [('305', '397')]
    }

    for page in sign_here_locations_2.keys():
        for location in range(len(sign_here_locations_2[page])):
            sign_here = docusign_esign.SignHere(document_id = '1', page_number = page, recipient_id = str(user.primary_key) + '01', tab_label = 'Sign Here', x_position = sign_here_locations_2[page][location][0], y_position = sign_here_locations_2[page][location][1])
            sign_here_tabs_2.append(sign_here)

    date_signed_tabs_2 = []
    date_signed_locations_2 = {
        '13': [('380', '420')]
    }

    for page in date_signed_locations_2.keys():
        for location in range(len(date_signed_locations_2[page])):
            date_signed = docusign_esign.DateSigned(document_id = '1', page_number = page, recipient_id = str(user.primary_key) + '01', x_position = date_signed_locations_2[page][location][0], y_position = date_signed_locations_2[page][location][1])
            date_signed_tabs_2.append(date_signed)

    signer_1.tabs = docusign_esign.Tabs(sign_here_tabs = sign_here_tabs_1, date_signed_tabs = date_signed_tabs_1)
    signer_2.tabs = docusign_esign.Tabs(sign_here_tabs = sign_here_tabs_2, date_signed_tabs = date_signed_tabs_2)

    envelope_definition = docusign_esign.EnvelopeDefinition(
        email_subject = "Buyers Offer Agreement",
        documents = [document],
        recipients = docusign_esign.Recipients(signers = [signer_1, signer_2]),
        status = "sent"
    )

    api_client = docusign_esign.ApiClient()
    api_client.host = "https://demo.docusign.net/restapi"
    api_client.set_default_header("Authorization", "Bearer " + request.GET.get('token'))

    envelope_api = docusign_esign.EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id=CLIENT_ACCOUNT_ID, envelope_definition=envelope_definition)

    envelope_id = results.envelope_id

    if(buyers_offer_obj.envelope_id):
        r = requests.get(url="https://demo.docusign.net/restapi/v2.1/accounts/{0}/envelopes/{1}".format(CLIENT_ACCOUNT_ID, buyers_offer_obj.envelope_id), headers={'Authorization':"Bearer " + request.GET.get('token')})
        envelope_info = r.json()
        if envelope_info['status'] == "completed":
            document = envelope_api.get_document(CLIENT_ACCOUNT_ID, '1', buyers_offer_obj.envelope_id)
            shutil.move(document, 'buyers_offer/static/pdf/purchase_agreement_signed_' + user.primary_key + '.pdf')
            return HttpResponseRedirect(reverse('sign_complete'))
    else:
        buyers_offer_obj.envelope_id = envelope_id
        buyers_offer_obj.save()

    recipient_view_request_1 = docusign_esign.RecipientViewRequest(
        authentication_method = "None", client_user_id = '1', recipient_id = str(user.primary_key) + '00', return_url = request.build_absolute_uri(reverse('sign_completed')), user_name = signer_1_name, email = signer_1_email)

    results_1 = envelope_api.create_recipient_view(CLIENT_ACCOUNT_ID, buyers_offer_obj.envelope_id, recipient_view_request = recipient_view_request_1)

    recipient_view_request_2 = docusign_esign.RecipientViewRequest(
        authentication_method = "None", client_user_id = '1', recipient_id = str(user.primary_key) + '01', return_url = request.build_absolute_uri(reverse('sign_completed')), user_name = signer_2_name, email = signer_2_email)

    results_2 = envelope_api.create_recipient_view(CLIENT_ACCOUNT_ID, buyers_offer_obj.envelope_id, recipient_view_request = recipient_view_request_2)

    # Render the HTML template sign_completed.html
    return render(request, 'sign_here.html', context={'url_1': results_1.url, 'url_2': results_2.url})


@login_required
def sign_completed(request):
    """View function for the successful e-signature completion"""

    # Render the HTML template sign_completed.html
    return render(request, 'sign_completed.html')


@login_required
def sign_complete(request):
    """View function for the successful e-signature completions"""

    user = CustomUser.objects.get(pk=request.user.pk)

    # Render the HTML template sign_complete.html
    return render(request, 'sign_complete.html', {'pdf_path': 'pdf/purchase_agreement_signed_' + str(user.primary_key) +'.pdf'})