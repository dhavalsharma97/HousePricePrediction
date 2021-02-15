from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from helpers.helper import fill_pdf
from buyers_offer.forms import BuyersOfferForm, BuyersOfferForm1, BuyersOfferForm2
from buyers_offer.models import BuyersOffer

def index(request):
    """View function for home page of site"""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

    
def offer_form(request):
    """View function for buyers offer form page of site"""
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersOfferForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Save the record to database
            buyers_offer_obj = BuyersOffer(first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'],
                                        phone=form.cleaned_data['phone'],
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
            buyers_offer_obj.first_loan_type_other = form.cleaned_data['first_loan_type_other']
            buyers_offer_obj.second_loan_fixed_rate = form.cleaned_data['second_loan_fixed_rate']
            buyers_offer_obj.second_loan_adjustable_loan_rate = form.cleaned_data['second_loan_adjustable_loan_rate']
            buyers_offer_obj.second_loan_max_points = form.cleaned_data['second_loan_max_points']
            buyers_offer_obj.appraisal_contingency = form.cleaned_data['appraisal_contingency']
            buyers_offer_obj.appraisal_contingency_days = form.cleaned_data['appraisal_contingency_days']
            buyers_offer_obj.loan_prequalification_days = form.cleaned_data['loan_prequalification_days']
            buyers_offer_obj.loan_contingency = form.cleaned_data['loan_contingency']
            buyers_offer_obj.loan_contingency_days = form.cleaned_data['loan_contingency_days']
            buyers_offer_obj.save()

            # Saving the buyer details
            request.session['buyer'] = buyers_offer_obj.pk

            # Generate PDF
            fill_pdf('buyers_offer', 'purchase_agreement', request.session['buyer'])

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('offerformconfirm'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = BuyersOfferForm()

    context = {
        'form': form
    }

    return render(request, 'offer_form.html', context)


def offer_form_confirm(request):
    """View function for buyers offer confirmation page of site"""

    # Render the HTML template offer_form_confirm.html
    return render(request, 'offer_form_confirm.html')


def offer_form_1(request):
    """View function for buyers offer form page of site"""
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersOfferForm1(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Save the record to database
            buyers_offer_obj = BuyersOffer.objects.get(pk=request.session['buyer'])

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
            fill_pdf('buyers_offer', 'purchase_agreement', request.session['buyer'])

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('offerformconfirm1'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = BuyersOfferForm1()

    context = {
        'form': form
    }

    return render(request, 'offer_form_1.html', context)


def offer_form_confirm_1(request):
    """View function for buyers offer confirmation page of site"""

    # Render the HTML template offer_form_confirm.html
    return render(request, 'offer_form_confirm_1.html')


def offer_form_2(request):
    """View function for buyers offer form page of site"""
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersOfferForm2(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Save the record to database
            buyers_offer_obj = BuyersOffer.objects.get(pk=request.session['buyer'])

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
            fill_pdf('buyers_offer', 'purchase_agreement', request.session['buyer'])

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('offerformconfirm2'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = BuyersOfferForm2()

    context = {
        'form': form
    }

    return render(request, 'offer_form_2.html', context)


def offer_form_confirm_2(request):
    """View function for buyers offer confirmation page of site"""

    # Render the HTML template offer_form_confirm.html
    return render(request, 'offer_form_confirm_2.html')