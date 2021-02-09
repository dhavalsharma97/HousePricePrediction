from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from helpers.helper import fill_pdf
from buyers_offer.forms import BuyersOfferForm, BuyersOfferForm1
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
                                        down_payment=form.cleaned_data['down_payment'],
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

            if form.cleaned_data['buyer_agent']:
                buyers_offer_obj.buyer_brokerage_firm = form.cleaned_data['buyer_brokerage_firm']
                buyers_offer_obj.buyer_brokerage_license_number = form.cleaned_data['buyer_brokerage_license_number']
                buyers_offer_obj.buyer_agent_name = form.cleaned_data['buyer_agent_name']
                buyers_offer_obj.buyer_agent_license_number = form.cleaned_data['buyer_agent_license_number']

                if not form.cleaned_data['dual_brokerage']:
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