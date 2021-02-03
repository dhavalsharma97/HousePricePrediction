from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from helpers.helper import fill_pdf
from buyers_offer.forms import BuyersOfferForm
from buyers_offer.models import Buyer, Payment, PropertyAddress

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
            form_data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'offer_price': form.cleaned_data['offer_price'],
                'apartment': form.cleaned_data['apartment'],
                'street': form.cleaned_data['street'],
                'city': form.cleaned_data['city'],
                'county': form.cleaned_data['county'],
                'zipcode': form.cleaned_data['zipcode'],
                'parcel_number': form.cleaned_data['parcel_number'],
                'escrow_date': form.cleaned_data['escrow_date'],
                'escrow_days': form.cleaned_data['escrow_days'],
                'payment_type': form.cleaned_data['payment_type'],
                'down_payment': form.cleaned_data['down_payment']
            }

            record1 = Payment(payment_type=form_data['payment_type'], 
                            down_payment=form_data['down_payment'])
            record1.save()

            record2 = PropertyAddress(apartment=form_data['apartment'],
                                    street=form_data['street'],
                                    city=form_data['city'],
                                    county=form_data['county'],
                                    zipcode=form_data['zipcode'],
                                    parcel_number=form_data['parcel_number'])
            record2.save()

            record = Buyer(first_name=form_data['first_name'],
                            last_name=form_data['last_name'],
                            email=form_data['email'],
                            phone=form_data['phone'],
                            escrow_date=form_data['escrow_date'],
                            escrow_days=form_data['escrow_days'],
                            offer_price=form_data['offer_price'])
            record.save()
            
            record.payment.add(record1)
            record.property_address.add(record2)
            record.save()

            # Generate PDF
            fill_pdf('buyers_offer', 'purchase_agreement', form_data)

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