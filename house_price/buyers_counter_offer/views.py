from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import base64
import requests
from pdfminer.high_level import extract_text
from PIL import Image
import fitz
import docusign_esign
import shutil
import re
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

from buyers_counter_offer.models import BuyersCounterOffer
from buyers_counter_offer.forms import BuyersCounterOfferForm, BuyersCounterOfferForm1
from buyers_offer.models import CustomUser, BuyersOffer
from sellers_counter_offer.models import SellersCounterOffer
from helpers.helper import fill_pdf_2

CLIENT_AUTH_ID = '6dfb62a5-2b74-4358-81de-327243a9fe60'
CLIENT_SECRET_KEY = '75c8da9b-d4f0-4c06-a15c-2ab6815edf6b'
CLIENT_ACCOUNT_ID = '13197074'


@login_required
def get_access_code(request):
    """Helper function for getting the access code for e-signature"""

    base_url = "https://account-d.docusign.com/oauth/auth"
    auth_url = "{0}?response_type=code&scope=signature&client_id={1}&redirect_uri={2}".format(base_url, CLIENT_AUTH_ID, request.build_absolute_uri(reverse('buyerscounterofferauthlogin')))
    
    return HttpResponseRedirect(auth_url)


@login_required
def get_access_code_1(request):
    """Helper function for getting the access code for e-signature"""

    base_url = "https://account-d.docusign.com/oauth/auth"
    auth_url = "{0}?response_type=code&scope=signature&client_id={1}&redirect_uri={2}".format(base_url, CLIENT_AUTH_ID, request.build_absolute_uri(reverse('buyerscounterofferauthlogin1')))
    
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
        return HttpResponseRedirect("{0}?token={1}".format(reverse('buyerscounterform1'), response['access_token']))

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
        return HttpResponseRedirect("{0}?token={1}".format(reverse('buyerscounteroffersigningurl'), response['access_token']))

    return HttpResponse(response['error'])


@login_required
def buyers_counter_form(request):
    """View function for buyers counter offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        if BuyersCounterOffer.objects.filter(pk=user.primary_key_2).count() > 0:
            buyers_counter_offer_obj = BuyersCounterOffer.objects.get(pk=user.primary_key_2)
        else:
            # Save the record to database
            buyers_counter_offer_obj = BuyersCounterOffer()
            buyers_counter_offer_obj.save()

            # Saving the buyer details
            user.primary_key_2 = buyers_counter_offer_obj.pk
            user.save()

        if request.FILES.get('sellers_counter_offer'):
            sellers_counter_offer = request.FILES['sellers_counter_offer']
            with open('buyers_counter_offer/static/pdf/sellers_counter_offer_upload_'+ str(user.primary_key_2) + '.pdf', 'wb+') as destination:
                for chunk in sellers_counter_offer.chunks():
                    destination.write(chunk)

            sellers_counter_offer_text = extract_text('buyers_counter_offer/static/pdf/sellers_counter_offer_upload_' + str(user.primary_key_2) + '.pdf')
            envelope_id_location = re.search(r'(DocuSign Envelope ID: )\b', sellers_counter_offer_text)
            
            if envelope_id_location:
                envelope_id = sellers_counter_offer_text[envelope_id_location.end(): envelope_id_location.end() + 36]
                buyers_counter_offer_obj.envelope_id = envelope_id
                buyers_counter_offer_obj.save()

                # Getting the other terms
                doc = fitz.open('buyers_counter_offer/static/pdf/sellers_counter_offer_upload_' + str(user.primary_key_2) + '.pdf')
                page = doc.loadPage(0)
                pix = page.getPixmap()
                pix.writePNG('buyers_counter_offer/static/images/sellers_counter_offer_upload_' + str(user.primary_key_2) + '.png')
                image = Image.open('buyers_counter_offer/static/images/sellers_counter_offer_upload_' + str(user.primary_key_2) + '.png')
                cropped_image = image.crop((0, 193, 612, 330))
                cropped_image.save('buyers_counter_offer/static/images/sellers_counter_offer_upload_' + str(user.primary_key_2) + '.png')

                return HttpResponseRedirect(reverse('buyerscounterofferaccesscode'))
            else:
                return HttpResponseRedirect(reverse('buyerscounterformerror'))
        else:
            return HttpResponseRedirect(reverse('buyerscounterformerror'))
    
    return render(request, 'buyers_counter_form.html')


@login_required
def buyers_counter_form_1(request):
    """View function for buyers counter offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersCounterOfferForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            buyers_counter_offer_obj = BuyersCounterOffer.objects.get(pk=user.primary_key_2)
            buyers_counter_offer_obj.contract_sign_date = form.cleaned_data['contract_sign_date']
            buyers_counter_offer_obj.contract_offer = form.cleaned_data['contract_offer']
            buyers_counter_offer_obj.counter_offer = form.cleaned_data['counter_offer']
            buyers_counter_offer_obj.other_contract_offer = form.cleaned_data['other_contract_offer']
            buyers_counter_offer_obj.property_address = form.cleaned_data['property_address']
            buyers_counter_offer_obj.buyers_name = form.cleaned_data['buyers_name']
            buyers_counter_offer_obj.sellers_name = form.cleaned_data['sellers_name']
            buyers_counter_offer_obj.counter_offer_accept = form.cleaned_data['counter_offer_accept']
            buyers_counter_offer_obj.save()

            # Generate PDF
            if buyers_counter_offer_obj.counter_offer_accept:
                shutil.copy('buyers_counter_offer/static/pdf/sellers_counter_offer_upload_' + str(user.primary_key_2) + '.pdf', 'buyers_counter_offer/static/pdf/buyers_counter_offer_filled_' + str(user.primary_key_2) + '.pdf')

                # Redirect to a new URL:
                return HttpResponseRedirect(reverse('buyerscounterformconfirm'))
            
            return HttpResponseRedirect(reverse('buyerscounterform2'))

    # If this is a GET (or any other method) create the default form.
    else:
        buyers_counter_offer_obj = BuyersCounterOffer.objects.get(pk=user.primary_key_2)

        if request.GET.get('token'):
            r = requests.get(url="https://demo.docusign.net/restapi/v2.1/accounts/{0}/envelopes/{1}".format(CLIENT_ACCOUNT_ID, buyers_counter_offer_obj.envelope_id), headers={'Authorization':"Bearer " + request.GET.get('token')})
            envelope_info = r.json()
            r = requests.get(url="https://demo.docusign.net/restapi/v2.1/accounts/{0}/envelopes/{1}/recipients".format(CLIENT_ACCOUNT_ID, buyers_counter_offer_obj.envelope_id), headers={'Authorization':"Bearer " + request.GET.get('token')})
            signer_info = r.json()

            buyers_counter_offer_obj.sellers_id = signer_info['signers'][0]['recipientId'][:-2]
            sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=buyers_counter_offer_obj.sellers_id)
            buyers_offer_obj = BuyersOffer.objects.get(pk=sellers_counter_offer_obj.buyers_id)

            buyers_counter_offer_obj.contract_sign_date = envelope_info['completedDateTime'][:10]
            buyers_counter_offer_obj.property_address = buyers_offer_obj.apartment + " " + buyers_offer_obj.street + " " + buyers_offer_obj.city + " " + buyers_offer_obj.county + " " + str(buyers_offer_obj.zipcode)
            buyers_counter_offer_obj.buyers_name = buyers_offer_obj.first_name + " " + buyers_offer_obj.last_name
            buyers_counter_offer_obj.sellers_name = sellers_counter_offer_obj.sellers_name
            buyers_counter_offer_obj.save()

        form = BuyersCounterOfferForm(initial={
            'contract_sign_date': buyers_counter_offer_obj.contract_sign_date,
            'contract_offer': buyers_counter_offer_obj.contract_offer,
            'counter_offer': buyers_counter_offer_obj.counter_offer,
            'other_contract_offer': buyers_counter_offer_obj.other_contract_offer,
            'property_address': buyers_counter_offer_obj.property_address,
            'buyers_name': buyers_counter_offer_obj.buyers_name,
            'sellers_name': buyers_counter_offer_obj.sellers_name,
            'counter_offer_accept': buyers_counter_offer_obj.counter_offer_accept
        })

    context = {
        'form': form,
        'other_terms_path': 'images/sellers_counter_offer_upload_' + str(user.primary_key_2) +'.png'
    }

    return render(request, 'buyers_counter_form_1.html', context)


@login_required
def buyers_counter_form_2(request):
    """View function for buyers counter offer form page of site"""
    user = CustomUser.objects.get(pk=request.user.pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BuyersCounterOfferForm1(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            buyers_counter_offer_obj = BuyersCounterOffer.objects.get(pk=user.primary_key_2)
            buyers_counter_offer_obj.other_terms_text_1 = form.cleaned_data['other_terms_text_1']
            buyers_counter_offer_obj.other_terms_text_2 = form.cleaned_data['other_terms_text_2']
            buyers_counter_offer_obj.other_terms_text_3 = form.cleaned_data['other_terms_text_3']
            buyers_counter_offer_obj.other_terms_text_4 = form.cleaned_data['other_terms_text_4']
            buyers_counter_offer_obj.other_terms = form.cleaned_data['other_terms']
            buyers_counter_offer_obj.additional_terms = form.cleaned_data['additional_terms']
            buyers_counter_offer_obj.expiration_time = form.cleaned_data['expiration_time']
            buyers_counter_offer_obj.expiration_meridian = form.cleaned_data['expiration_meridian']
            buyers_counter_offer_obj.expiration_date = form.cleaned_data['expiration_date']
            buyers_counter_offer_obj.save()

            # Generate PDF
            fill_pdf_2('buyers_counter_offer', 'sellers_counter_offer_upload', str(user.primary_key_2))

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('buyerscounterformconfirm'))

    # If this is a GET (or any other method) create the default form.
    else:
        buyers_counter_offer_obj = BuyersCounterOffer.objects.get(pk=user.primary_key_2)

        form = BuyersCounterOfferForm1(initial={
            'other_terms_text_1': buyers_counter_offer_obj.other_terms_text_1,
            'other_terms_text_2': buyers_counter_offer_obj.other_terms_text_2,
            'other_terms_text_3': buyers_counter_offer_obj.other_terms_text_3,
            'other_terms_text_4': buyers_counter_offer_obj.other_terms_text_4,
            'other_terms': buyers_counter_offer_obj.other_terms,
            'additional_terms': buyers_counter_offer_obj.additional_terms,
            'expiration_time': buyers_counter_offer_obj.expiration_time,
            'expiration_meridian': buyers_counter_offer_obj.expiration_meridian,
            'expiration_date': buyers_counter_offer_obj.expiration_date
        })

    context = {
        'form': form
    }

    return render(request, 'buyers_counter_form_2.html', context)


@login_required
def counter_form_confirm(request):
    """View function for buyers counter offer form confirmation page of site"""

    user = CustomUser.objects.get(pk=request.user.pk)
    
    return render(request, 'buyers_counter_form_confirm.html', {'pdf_path': 'pdf/buyers_counter_offer_filled_' + str(user.primary_key_2) +'.pdf'})


@login_required
def buyers_counter_form_error(request):
    """View function for buyers counter offer form error page of site"""
    
    return render(request, 'buyers_counter_form_error.html')


@login_required
def embedded_signing_ceremony(request):
    """View function for the e-signature request"""

    user = CustomUser.objects.get(pk=request.user.pk)
    buyers_counter_offer_obj = BuyersCounterOffer.objects.get(pk=user.primary_key_2)
    sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=buyers_counter_offer_obj.sellers_id)
    buyers_offer_obj = BuyersOffer.objects.get(pk=sellers_counter_offer_obj.buyers_id)
    signer_1_name = buyers_offer_obj.first_name + " " + buyers_offer_obj.last_name
    signer_1_email = buyers_offer_obj.email
    signer_2_name = buyers_offer_obj.spouse_first_name + " " + buyers_offer_obj.spouse_last_name
    signer_2_email = buyers_offer_obj.spouse_email

    with open(os.path.join(BASE_DIR, 'static/pdf', 'buyers_counter_offer_filled_' + str(user.primary_key_2) + '.pdf'), "rb") as file:
        content_bytes = file.read()

    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    document = docusign_esign.Document(
        document_base64 = base64_file_content,
        name = 'Buyers Counter Offer Document',
        file_extension = 'pdf',
        document_id = '1'
    )

    if not sellers_counter_offer_obj.multiple_offers:
        sign_here_locations_1 = {
            '1': [('78', '503')]
        }

        date_signed_locations_1 = {
            '1': [('410', '515')]
        }

        sign_here_locations_2 = {
            '1': [('157', '514')]
        }

        date_signed_locations_2 = {
            '1': [('410', '534')]
        }
    else:
        sign_here_locations_1 = {
            '1': [('51', '416')]
        }

        date_signed_locations_1 = {
            '1': [('528', '437')]
        }

        sign_here_locations_2 = {
            '1': [('130', '428')]
        }

        date_signed_locations_2 = {
            '1': [('528', '449')]
        }

    signer_1 = docusign_esign.Signer(email = signer_1_email, name = signer_1_name, recipient_id = str(user.primary_key_2) + '00', routing_order = '1', client_user_id = '1')
    sign_here_tabs_1 = []

    for page in sign_here_locations_1.keys():
        for location in range(len(sign_here_locations_1[page])):
            sign_here = docusign_esign.SignHere(document_id = '1', page_number = page, recipient_id = str(user.primary_key_2) + '00', tab_label = 'Sign Here', x_position = sign_here_locations_1[page][location][0], y_position = sign_here_locations_1[page][location][1])
            sign_here_tabs_1.append(sign_here)

    date_signed_tabs_1 = []

    for page in date_signed_locations_1.keys():
        for location in range(len(date_signed_locations_1[page])):
            date_signed = docusign_esign.DateSigned(document_id = '1', page_number = page, recipient_id = str(user.primary_key_2) + '00', x_position = date_signed_locations_1[page][location][0], y_position = date_signed_locations_1[page][location][1])
            date_signed_tabs_1.append(date_signed)

    signer_2 = docusign_esign.Signer(email = signer_2_email, name = signer_2_name, recipient_id = str(user.primary_key_2) + '01', routing_order = '1', client_user_id = '1')
    sign_here_tabs_2 = []

    for page in sign_here_locations_2.keys():
        for location in range(len(sign_here_locations_2[page])):
            sign_here = docusign_esign.SignHere(document_id = '1', page_number = page, recipient_id = str(user.primary_key_2) + '01', tab_label = 'Sign Here', x_position = sign_here_locations_2[page][location][0], y_position = sign_here_locations_2[page][location][1])
            sign_here_tabs_2.append(sign_here)

    date_signed_tabs_2 = []

    for page in date_signed_locations_2.keys():
        for location in range(len(date_signed_locations_2[page])):
            date_signed = docusign_esign.DateSigned(document_id = '1', page_number = page, recipient_id = str(user.primary_key_2) + '01', x_position = date_signed_locations_2[page][location][0], y_position = date_signed_locations_2[page][location][1])
            date_signed_tabs_2.append(date_signed)

    signer_1.tabs = docusign_esign.Tabs(sign_here_tabs = sign_here_tabs_1, date_signed_tabs = date_signed_tabs_1)
    signer_2.tabs = docusign_esign.Tabs(sign_here_tabs = sign_here_tabs_2, date_signed_tabs = date_signed_tabs_2)

    envelope_definition = docusign_esign.EnvelopeDefinition(
        email_subject = "Buyers Counter Offer Agreement",
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

    if(buyers_counter_offer_obj.envelope_id_1):
        r = requests.get(url="https://demo.docusign.net/restapi/v2.1/accounts/{0}/envelopes/{1}".format(CLIENT_ACCOUNT_ID, buyers_counter_offer_obj.envelope_id_1), headers={'Authorization':"Bearer " + request.GET.get('token')})
        envelope_info = r.json()
        
        if envelope_info['status'] == "completed":
            document = envelope_api.get_document(CLIENT_ACCOUNT_ID, '1', buyers_counter_offer_obj.envelope_id_1)
            shutil.move(document, 'buyers_counter_offer/static/pdf/buyers_counter_offer_signed_' + str(user.primary_key_2) + '.pdf')
            return HttpResponseRedirect(reverse('buyerscounteroffersigncomplete'))
    else:
        buyers_counter_offer_obj.envelope_id_1 = envelope_id
        buyers_counter_offer_obj.save()

    recipient_view_request_1 = docusign_esign.RecipientViewRequest(
        authentication_method = "None", client_user_id = '1', recipient_id = str(user.primary_key_2) + '00', return_url = request.build_absolute_uri(reverse('buyerscounteroffersigncompleted')), user_name = signer_1_name, email = signer_1_email)

    results_1 = envelope_api.create_recipient_view(CLIENT_ACCOUNT_ID, buyers_counter_offer_obj.envelope_id_1, recipient_view_request = recipient_view_request_1)

    recipient_view_request_2 = docusign_esign.RecipientViewRequest(
        authentication_method = "None", client_user_id = '1', recipient_id = str(user.primary_key_2) + '01', return_url = request.build_absolute_uri(reverse('buyerscounteroffersigncompleted')), user_name = signer_2_name, email = signer_2_email)

    results_2 = envelope_api.create_recipient_view(CLIENT_ACCOUNT_ID, buyers_counter_offer_obj.envelope_id_1, recipient_view_request = recipient_view_request_2)

    # Render the HTML template sign_completed.html
    return render(request, 'buyers_counter_offer_sign_here.html', context={'url_1': results_1.url, 'url_2': results_2.url})


@login_required
def sign_completed(request):
    """View function for the successful e-signature completion"""

    # Render the HTML template sign_completed.html
    return render(request, 'buyers_counter_offer_sign_completed.html')


@login_required
def sign_complete(request):
    """View function for the successful e-signature completions"""

    user = CustomUser.objects.get(pk=request.user.pk)

    # Render the HTML template sign_complete.html
    return render(request, 'buyers_counter_offer_sign_complete.html', {'pdf_path': 'pdf/buyers_counter_offer_signed_' + str(user.primary_key_2) +'.pdf'})