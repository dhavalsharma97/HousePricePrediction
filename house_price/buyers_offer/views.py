from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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
            record1 = Payment(payment_type=form.cleaned_data['payment_type'], 
                            down_payment=form.cleaned_data['down_payment'])
            record1.save()

            record2 = PropertyAddress(apartment=form.cleaned_data['apartment'],
                                    street=form.cleaned_data['street'],
                                    city=form.cleaned_data['city'],
                                    state=form.cleaned_data['state'],
                                    country=form.cleaned_data['country'],
                                    pincode=form.cleaned_data['pincode'])
            record2.save()

            record = Buyer(first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email'],
                            phone=form.cleaned_data['phone'],
                            offer_price=form.cleaned_data['offer_price'])
            record.save()
            
            record.payment.add(record1)
            record.property_address.add(record2)
            record.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = BuyersOfferForm()

    context = {
        'form': form
    }

    return render(request, 'offer_form.html', context)