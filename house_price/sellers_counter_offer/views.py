from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import base64
import requests
from pdfminer.high_level import extract_text
import re

from sellers_counter_offer.models import SellersCounterOffer
from sellers_counter_offer.forms import SellersCounterOfferForm
from buyers_offer.models import CustomUser, BuyersOffer

CLIENT_AUTH_ID = '6dfb62a5-2b74-4358-81de-327243a9fe60'
CLIENT_SECRET_KEY = '75c8da9b-d4f0-4c06-a15c-2ab6815edf6b'
CLIENT_ACCOUNT_ID = '13197074'


@login_required
def get_access_code(request):
    """Helper function for getting the access code for e-signature"""

    base_url = "https://account-d.docusign.com/oauth/auth"
    auth_url = "{0}?response_type=code&scope=signature&client_id={1}&redirect_uri={2}".format(base_url, CLIENT_AUTH_ID, request.build_absolute_uri(reverse('authlogin')))

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
        return HttpResponseRedirect("{0}?token={1}".format(reverse('sellerscounterform1'), response['access_token']))

    return HttpResponse(response['error'])


@login_required
def sellers_counter_form(request):
    """View function for sellers counter offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        if SellersCounterOffer.objects.filter(pk=user.primary_key).count() > 0:
            sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=user.primary_key)
        else:
            # Save the record to database
            sellers_counter_offer_obj = SellersCounterOffer()
            sellers_counter_offer_obj.save()

            # Saving the seller details
            user.primary_key = sellers_counter_offer_obj.pk
            user.save()

        if request.FILES.get('purchase_agreement'):
            purchase_agreement = request.FILES['purchase_agreement']
            with open('sellers_counter_offer/static/pdf/purchase_agreement_upload_'+ user.primary_key + '.pdf', 'wb+') as destination:
                for chunk in purchase_agreement.chunks():
                    destination.write(chunk)

            purchase_agreement_text = extract_text('sellers_counter_offer/static/pdf/purchase_agreement_upload_' + user.primary_key + '.pdf')
            envelope_id_location = re.search(r'\b(DocuSign Envelope ID: )\b', purchase_agreement_text)
            
            if envelope_id_location:
                envelope_id = purchase_agreement_text[envelope_id_location.end(): envelope_id_location.end() + 36]
                sellers_counter_offer_obj.envelope_id = envelope_id
                sellers_counter_offer_obj.save()

                return HttpResponseRedirect(reverse('getaccesscode'))
            else:
                return HttpResponseRedirect(reverse('sellerscounterformerror'))
        else:
            return HttpResponseRedirect(reverse('sellerscounterformerror'))
    
    return render(request, 'sellers_counter_form.html')


@login_required
def sellers_counter_form_1(request):
    """View function for sellers counter offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = SellersCounterOfferForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=user.primary_key)  
            sellers_counter_offer_obj.contract_sign_date = form.cleaned_data['contract_sign_date']
            sellers_counter_offer_obj.multiple_offers = form.cleaned_data['multiple_offers']
            sellers_counter_offer_obj.contract_offer = form.cleaned_data['contract_offer']
            sellers_counter_offer_obj.counter_offer = form.cleaned_data['counter_offer']
            sellers_counter_offer_obj.property_address = form.cleaned_data['property_address']
            sellers_counter_offer_obj.buyers_name = form.cleaned_data['buyers_name']
            sellers_counter_offer_obj.sellers_name = form.cleaned_data['sellers_name']
            sellers_counter_offer_obj.offer_price_change = form.cleaned_data['offer_price_change']
            sellers_counter_offer_obj.new_offer_price = form.cleaned_data['new_offer_price']
            sellers_counter_offer_obj.escrow_company_change = form.cleaned_data['escrow_company_change']
            sellers_counter_offer_obj.escrow_company_name = form.cleaned_data['escrow_company_name']
            sellers_counter_offer_obj.title_company_change = form.cleaned_data['title_company_change']
            sellers_counter_offer_obj.title_company_name = form.cleaned_data['title_company_name']
            sellers_counter_offer_obj.termite_company_change = form.cleaned_data['termite_company_change']
            sellers_counter_offer_obj.termite_company_name = form.cleaned_data['termite_company_name']
            sellers_counter_offer_obj.other_terms = form.cleaned_data['other_terms']
            sellers_counter_offer_obj.other_terms_text = form.cleaned_data['other_terms_text']
            sellers_counter_offer_obj.remove_appraisal_contingence = form.cleaned_data['remove_appraisal_contingence']
            sellers_counter_offer_obj.remove_inspection_contingence = form.cleaned_data['remove_inspection_contingence']
            sellers_counter_offer_obj.loan_qualification_proofs = form.cleaned_data['loan_qualification_proofs']
            sellers_counter_offer_obj.addenda = form.cleaned_data['addenda']
            sellers_counter_offer_obj.addenda_name_1 = form.cleaned_data['addenda_name_1']
            sellers_counter_offer_obj.addenda_name_2 = form.cleaned_data['addenda_name_2']
            sellers_counter_offer_obj.addenda_name_3 = form.cleaned_data['addenda_name_3']
            sellers_counter_offer_obj.expiration_time = form.cleaned_data['expiration_time']
            sellers_counter_offer_obj.expiration_meridian = form.cleaned_data['expiration_meridian']
            sellers_counter_offer_obj.expiration_date = form.cleaned_data['expiration_date']
            sellers_counter_offer_obj.save()

            # Generate PDF
            # fill_pdf('sellers_counter_offer', 'purchase_agreement', user.primary_key)

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('counterformconfirm'))

    # If this is a GET (or any other method) create the default form.
    else:
        sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=user.primary_key)

        r = requests.get(url="https://demo.docusign.net/restapi/v2.1/accounts/{0}/envelopes/{1}".format(CLIENT_ACCOUNT_ID, sellers_counter_offer_obj.envelope_id), headers={'Authorization':"Bearer " + request.GET.get('token')})
        envelope_info = r.json()
        r = requests.get(url="https://demo.docusign.net/restapi/v2.1/accounts/{0}/envelopes/{1}/recipients".format(CLIENT_ACCOUNT_ID, sellers_counter_offer_obj.envelope_id), headers={'Authorization':"Bearer " + request.GET.get('token')})
        signer_info = r.json()

        sellers_counter_offer_obj.buyers_id = signer_info['signers'][0]['recipientId'][:-2]
        buyers_offer_obj = BuyersOffer.objects.get(pk=sellers_counter_offer_obj.buyers_id)

        sellers_counter_offer_obj.contract_sign_date = envelope_info['completedDateTime'][:10]
        sellers_counter_offer_obj.property_address = buyers_offer_obj.apartment + " " + buyers_offer_obj.street + " " + buyers_offer_obj.city + " " + buyers_offer_obj.county + " " + str(buyers_offer_obj.zipcode)
        sellers_counter_offer_obj.buyers_name = buyers_offer_obj.first_name + " " + buyers_offer_obj.last_name
        sellers_counter_offer_obj.title_company_name = buyers_offer_obj.title_policy

        form = SellersCounterOfferForm(initial={
            'contract_sign_date': sellers_counter_offer_obj.contract_sign_date,
            'multiple_offers': sellers_counter_offer_obj.multiple_offers,
            'contract_offer': sellers_counter_offer_obj.contract_offer,
            'counter_offer': sellers_counter_offer_obj.counter_offer,
            'property_address': sellers_counter_offer_obj.property_address,
            'buyers_name': sellers_counter_offer_obj.buyers_name,
            'sellers_name': sellers_counter_offer_obj.sellers_name,
            'offer_price_change': sellers_counter_offer_obj.offer_price_change,
            'new_offer_price': sellers_counter_offer_obj.new_offer_price,
            'escrow_company_change': sellers_counter_offer_obj.escrow_company_change,
            'escrow_company_name': sellers_counter_offer_obj.escrow_company_name,
            'title_company_change': sellers_counter_offer_obj.title_company_change,
            'title_company_name': sellers_counter_offer_obj.title_company_name,
            'termite_company_change': sellers_counter_offer_obj.termite_company_change,
            'termite_company_name': sellers_counter_offer_obj.termite_company_name,
            'other_terms': sellers_counter_offer_obj.other_terms,
            'other_terms_text': sellers_counter_offer_obj.other_terms_text,
            'remove_appraisal_contingence': sellers_counter_offer_obj.remove_appraisal_contingence,
            'remove_inspection_contingence': sellers_counter_offer_obj.remove_inspection_contingence,
            'loan_qualification_proofs': sellers_counter_offer_obj.loan_qualification_proofs,
            'addenda': sellers_counter_offer_obj.addenda,
            'addenda_name_1': sellers_counter_offer_obj.addenda_name_1,
            'addenda_name_2': sellers_counter_offer_obj.addenda_name_2,
            'addenda_name_3': sellers_counter_offer_obj.addenda_name_3,
            'expiration_time': sellers_counter_offer_obj.expiration_time,
            'expiration_meridian': sellers_counter_offer_obj.expiration_meridian,
            'expiration_date': sellers_counter_offer_obj.expiration_date
        })

    context = {
        'form': form
    }

    return render(request, 'sellers_counter_form_1.html', context)


@login_required
def counter_form_confirm(request):
    """View function for sellers counter offer form confirmation page of site"""
    
    return render(request, 'counter_form_confirm.html')


@login_required
def sellers_counter_form_error(request):
    """View function for sellers counter offer form error page of site"""
    
    return render(request, 'sellers_counter_form_error.html')