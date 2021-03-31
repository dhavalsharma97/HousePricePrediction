from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import base64
import requests
from pdfminer.high_level import extract_text
import docusign_esign
import shutil
import re
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

from sellers_counter_offer.models import SellersCounterOffer
from sellers_counter_offer.forms import SellersCounterOfferForm
from buyers_offer.models import CustomUser, BuyersOffer
from helpers.helper import fill_pdf_1

CLIENT_AUTH_ID = '6dfb62a5-2b74-4358-81de-327243a9fe60'
CLIENT_SECRET_KEY = '75c8da9b-d4f0-4c06-a15c-2ab6815edf6b'
CLIENT_ACCOUNT_ID = '13197074'


@login_required
def get_access_code(request):
    """Helper function for getting the access code for e-signature"""

    base_url = "https://account-d.docusign.com/oauth/auth"
    auth_url = "{0}?response_type=code&scope=signature&client_id={1}&redirect_uri={2}".format(base_url, CLIENT_AUTH_ID, request.build_absolute_uri(reverse('sellerscounterofferauthlogin')))
    
    return HttpResponseRedirect(auth_url)


@login_required
def get_access_code_1(request):
    """Helper function for getting the access code for e-signature"""

    base_url = "https://account-d.docusign.com/oauth/auth"
    auth_url = "{0}?response_type=code&scope=signature&client_id={1}&redirect_uri={2}".format(base_url, CLIENT_AUTH_ID, request.build_absolute_uri(reverse('sellerscounterofferauthlogin1')))
    
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
def auth_login_1(request):
    """Helper function for authenticating the user for e-signature"""

    base_url = "https://account-d.docusign.com/oauth/token"
    auth_code_string = "{0}:{1}".format(CLIENT_AUTH_ID, CLIENT_SECRET_KEY)
    auth_token = base64.b64encode(auth_code_string.encode())

    req_headers = {"Authorization": "Basic {0}".format(auth_token.decode('utf-8'))}
    post_data = {"grant_type": "authorization_code", "code": request.GET.get('code')}

    r = requests.post(base_url, data=post_data, headers=req_headers)

    response = r.json()

    if not 'error' in response:
        return HttpResponseRedirect("{0}?token={1}".format(reverse('sellerscounteroffersigningurl'), response['access_token']))

    return HttpResponse(response['error'])


@login_required
def sellers_counter_form(request):
    """View function for sellers counter offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        if SellersCounterOffer.objects.filter(pk=user.primary_key_1).count() > 0:
            sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=user.primary_key_1)
        else:
            # Save the record to database
            sellers_counter_offer_obj = SellersCounterOffer()
            sellers_counter_offer_obj.save()

            # Saving the seller details
            user.primary_key_1 = sellers_counter_offer_obj.pk
            user.save()

        if request.FILES.get('purchase_agreement'):
            purchase_agreement = request.FILES['purchase_agreement']
            with open('sellers_counter_offer/static/pdf/purchase_agreement_upload_'+ str(user.primary_key_1) + '.pdf', 'wb+') as destination:
                for chunk in purchase_agreement.chunks():
                    destination.write(chunk)

            purchase_agreement_text = extract_text('sellers_counter_offer/static/pdf/purchase_agreement_upload_' + str(user.primary_key_1) + '.pdf')
            envelope_id_location = re.search(r'\b(DocuSign Envelope ID: )\b', purchase_agreement_text)
            
            if envelope_id_location:
                envelope_id = purchase_agreement_text[envelope_id_location.end(): envelope_id_location.end() + 36]
                sellers_counter_offer_obj.envelope_id = envelope_id
                sellers_counter_offer_obj.save()

                return HttpResponseRedirect(reverse('sellerscounterofferaccesscode'))
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
            sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=user.primary_key_1)
            sellers_counter_offer_obj.contract_sign_date = form.cleaned_data['contract_sign_date']
            sellers_counter_offer_obj.multiple_offers = form.cleaned_data['multiple_offers']
            sellers_counter_offer_obj.contract_offer = form.cleaned_data['contract_offer']
            sellers_counter_offer_obj.counter_offer = form.cleaned_data['counter_offer']
            sellers_counter_offer_obj.other_contract_offer = form.cleaned_data['other_contract_offer']
            sellers_counter_offer_obj.property_address = form.cleaned_data['property_address']
            sellers_counter_offer_obj.buyers_name = form.cleaned_data['buyers_name']
            sellers_counter_offer_obj.sellers_name = form.cleaned_data['sellers_name']
            sellers_counter_offer_obj.sellers_email = form.cleaned_data['sellers_email']
            sellers_counter_offer_obj.sellers_spouse_name = form.cleaned_data['sellers_spouse_name']
            sellers_counter_offer_obj.sellers_spouse_email = form.cleaned_data['sellers_spouse_email']
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
            if not sellers_counter_offer_obj.multiple_offers:
                fill_pdf_1('sellers_counter_offer', 'sellers_counter_offer', str(user.primary_key_1))
            else:
                fill_pdf_1('sellers_counter_offer', 'sellers_multiple_counter_offer', str(user.primary_key_1))

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('sellerscounterformconfirm'))

    # If this is a GET (or any other method) create the default form.
    else:
        sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=user.primary_key_1)

        if request.GET.get('token'):
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
            sellers_counter_offer_obj.save()

        form = SellersCounterOfferForm(initial={
            'contract_sign_date': sellers_counter_offer_obj.contract_sign_date,
            'multiple_offers': sellers_counter_offer_obj.multiple_offers,
            'contract_offer': sellers_counter_offer_obj.contract_offer,
            'counter_offer': sellers_counter_offer_obj.counter_offer,
            'other_contract_offer': sellers_counter_offer_obj.other_contract_offer,
            'property_address': sellers_counter_offer_obj.property_address,
            'buyers_name': sellers_counter_offer_obj.buyers_name,
            'sellers_name': sellers_counter_offer_obj.sellers_name,
            'sellers_email': sellers_counter_offer_obj.sellers_email,
            'sellers_spouse_name': sellers_counter_offer_obj.sellers_spouse_name,
            'sellers_spouse_email': sellers_counter_offer_obj.sellers_spouse_email,
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

    user = CustomUser.objects.get(pk=request.user.pk)
    
    return render(request, 'counter_form_confirm.html', {'pdf_path': 'pdf/sellers_counter_offer_filled_' + str(user.primary_key_1) +'.pdf'})


@login_required
def sellers_counter_form_error(request):
    """View function for sellers counter offer form error page of site"""
    
    return render(request, 'sellers_counter_form_error.html')


@login_required
def embedded_signing_ceremony(request):
    """View function for the e-signature request"""

    user = CustomUser.objects.get(pk=request.user.pk)
    sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=user.primary_key_1)
    signer_1_name = sellers_counter_offer_obj.sellers_name
    signer_1_email = sellers_counter_offer_obj.sellers_email
    signer_2_name = sellers_counter_offer_obj.sellers_spouse_name
    signer_2_email = sellers_counter_offer_obj.sellers_spouse_email

    with open(os.path.join(BASE_DIR, 'static/pdf', 'sellers_counter_offer_filled_' + str(user.primary_key_1) + '.pdf'), "rb") as file:
        content_bytes = file.read()

    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    document = docusign_esign.Document(
        document_base64 = base64_file_content,
        name = 'Sellers Counter Offer Document',
        file_extension = 'pdf',
        document_id = '1'
    )

    if not sellers_counter_offer_obj.multiple_offers:
        sign_here_locations_1 = {
            '1': [('78', '456')]
        }

        date_signed_locations_1 = {
            '1': [('515', '478')]
        }

        sign_here_locations_2 = {
            '1': [('157', '466')]
        }

        date_signed_locations_2 = {
            '1': [('515', '488')]
        }
    else:
        sign_here_locations_1 = {
            '1': [('51', '370')]
        }

        date_signed_locations_1 = {
            '1': [('528', '391')]
        }

        sign_here_locations_2 = {
            '1': [('130', '382')]
        }

        date_signed_locations_2 = {
            '1': [('528', '403')]
        }

    signer_1 = docusign_esign.Signer(email = signer_1_email, name = signer_1_name, recipient_id = str(user.primary_key_1) + '00', routing_order = '1', client_user_id = '1')
    sign_here_tabs_1 = []

    for page in sign_here_locations_1.keys():
        for location in range(len(sign_here_locations_1[page])):
            sign_here = docusign_esign.SignHere(document_id = '1', page_number = page, recipient_id = str(user.primary_key_1) + '00', tab_label = 'Sign Here', x_position = sign_here_locations_1[page][location][0], y_position = sign_here_locations_1[page][location][1])
            sign_here_tabs_1.append(sign_here)

    date_signed_tabs_1 = []

    for page in date_signed_locations_1.keys():
        for location in range(len(date_signed_locations_1[page])):
            date_signed = docusign_esign.DateSigned(document_id = '1', page_number = page, recipient_id = str(user.primary_key_1) + '00', x_position = date_signed_locations_1[page][location][0], y_position = date_signed_locations_1[page][location][1])
            date_signed_tabs_1.append(date_signed)

    signer_2 = docusign_esign.Signer(email = signer_2_email, name = signer_2_name, recipient_id = str(user.primary_key_1) + '01', routing_order = '1', client_user_id = '1')
    sign_here_tabs_2 = []

    for page in sign_here_locations_2.keys():
        for location in range(len(sign_here_locations_2[page])):
            sign_here = docusign_esign.SignHere(document_id = '1', page_number = page, recipient_id = str(user.primary_key_1) + '01', tab_label = 'Sign Here', x_position = sign_here_locations_2[page][location][0], y_position = sign_here_locations_2[page][location][1])
            sign_here_tabs_2.append(sign_here)

    date_signed_tabs_2 = []

    for page in date_signed_locations_2.keys():
        for location in range(len(date_signed_locations_2[page])):
            date_signed = docusign_esign.DateSigned(document_id = '1', page_number = page, recipient_id = str(user.primary_key_1) + '01', x_position = date_signed_locations_2[page][location][0], y_position = date_signed_locations_2[page][location][1])
            date_signed_tabs_2.append(date_signed)

    signer_1.tabs = docusign_esign.Tabs(sign_here_tabs = sign_here_tabs_1, date_signed_tabs = date_signed_tabs_1)
    signer_2.tabs = docusign_esign.Tabs(sign_here_tabs = sign_here_tabs_2, date_signed_tabs = date_signed_tabs_2)

    envelope_definition = docusign_esign.EnvelopeDefinition(
        email_subject = "Sellers Counter Offer Agreement",
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

    if(sellers_counter_offer_obj.envelope_id_1):
        r = requests.get(url="https://demo.docusign.net/restapi/v2.1/accounts/{0}/envelopes/{1}".format(CLIENT_ACCOUNT_ID, sellers_counter_offer_obj.envelope_id_1), headers={'Authorization':"Bearer " + request.GET.get('token')})
        envelope_info = r.json()
        
        if envelope_info['status'] == "completed":
            document = envelope_api.get_document(CLIENT_ACCOUNT_ID, '1', sellers_counter_offer_obj.envelope_id_1)
            shutil.move(document, 'sellers_counter_offer/static/pdf/sellers_counter_offer_signed_' + str(user.primary_key_1) + '.pdf')
            return HttpResponseRedirect(reverse('sellerscounteroffersigncomplete'))
    else:
        sellers_counter_offer_obj.envelope_id_1 = envelope_id
        sellers_counter_offer_obj.save()

    recipient_view_request_1 = docusign_esign.RecipientViewRequest(
        authentication_method = "None", client_user_id = '1', recipient_id = str(user.primary_key_1) + '00', return_url = request.build_absolute_uri(reverse('sellerscounteroffersigncompleted')), user_name = signer_1_name, email = signer_1_email)

    results_1 = envelope_api.create_recipient_view(CLIENT_ACCOUNT_ID, sellers_counter_offer_obj.envelope_id_1, recipient_view_request = recipient_view_request_1)

    recipient_view_request_2 = docusign_esign.RecipientViewRequest(
        authentication_method = "None", client_user_id = '1', recipient_id = str(user.primary_key_1) + '01', return_url = request.build_absolute_uri(reverse('sellerscounteroffersigncompleted')), user_name = signer_2_name, email = signer_2_email)

    results_2 = envelope_api.create_recipient_view(CLIENT_ACCOUNT_ID, sellers_counter_offer_obj.envelope_id_1, recipient_view_request = recipient_view_request_2)

    # Render the HTML template sign_completed.html
    return render(request, 'sellers_counter_offer_sign_here.html', context={'url_1': results_1.url, 'url_2': results_2.url})


@login_required
def sign_completed(request):
    """View function for the successful e-signature completion"""

    # Render the HTML template sign_completed.html
    return render(request, 'sellers_counter_offer_sign_completed.html')


@login_required
def sign_complete(request):
    """View function for the successful e-signature completions"""

    user = CustomUser.objects.get(pk=request.user.pk)

    # Render the HTML template sign_complete.html
    return render(request, 'sellers_counter_offer_sign_complete.html', {'pdf_path': 'pdf/sellers_counter_offer_signed_' + str(user.primary_key_1) +'.pdf'})