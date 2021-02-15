from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from datetime import date
from num2words import num2words

from buyers_offer.models import BuyersOffer

def set_need_appearances_writer(writer: PdfFileWriter):
    try:
        catalog = writer._root_object
        
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)
            })

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)

        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer

def tick_buttons(page, fields):
    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].getObject()
        for field in fields:
            if writer_annot.get('/T') == field:
                writer_annot.update({
                    NameObject('/V'): NameObject(fields[field]),
                    NameObject('/AS'): NameObject(fields[field])
                })

def fill_pdf(application_name, pdf_name, buyer_id):
    buyers_offer_obj = BuyersOffer.objects.get(pk=buyer_id)
    
    data_1 = {
        'Date Prepared': date.today(),
        'A THIS IS AN OFFER FROM': buyers_offer_obj.first_name + ' ' + buyers_offer_obj.last_name,
        'property to be acquired': buyers_offer_obj.apartment + ' ' + buyers_offer_obj.street,
        'city': buyers_offer_obj.city,
        'county': buyers_offer_obj.county,
        'zip code': buyers_offer_obj.zipcode,
        'purchase price': num2words(buyers_offer_obj.offer_price),
        'dollars': buyers_offer_obj.offer_price,
        'parcel number': buyers_offer_obj.parcel_number
    }

    # Check Box - /Yes
    # Button - /On
    data_2 = {}

    # Cash Payment
    if buyers_offer_obj.payment_type == "Cash":
        if buyers_offer_obj.fund_verification == "Attached with this agreement":
            data_2['Check Box6'] = '/Yes'
        else:
            data_2['Check Box7'] = '/Yes'
            data_1['all cash offer number of days'] = buyers_offer_obj.fund_verification_other
    # Loan Payment
    else:
        data_1['first loan amount'] = buyers_offer_obj.first_loan_amount
        
        if buyers_offer_obj.first_loan_type == "FHA":
            data_2['Check Box8'] = '/Yes'
        elif buyers_offer_obj.first_loan_type == "VA":
            data_2['Check Box9'] = '/Yes'
        elif buyers_offer_obj.first_loan_type == "Seller Financing":
            data_2['Check Box10'] = '/Yes'
        elif buyers_offer_obj.first_loan_type == "AFA":
            data_2['Check Box11'] = '/Yes'
        elif buyers_offer_obj.first_loan_type == "Other":
            data_2['Check Box12'] = '/Yes'
            data_1['other type of first loan financing'] = buyers_offer_obj.first_loan_type_other
        
        data_1['first loan fixed rate'] = buyers_offer_obj.first_loan_fixed_rate
        data_1['first loan adjustable rate'] = buyers_offer_obj.first_loan_adjustable_loan_rate
        data_1['shall pay points not to exceed'] = buyers_offer_obj.first_loan_max_points
        data_1['BALANCE OF DOWN PAYMENT OR PURCHASE PRICE in the amount of'] = buyers_offer_obj.down_payment

        if buyers_offer_obj.second_loan:
            data_2['Check Box14'] = '/Yes'
            data_1['second load amount'] = buyers_offer_obj.second_loan_amount
        
        if buyers_offer_obj.second_loan_type == "Seller Financing":
            data_2['Check Box16'] = '/Yes'
        elif buyers_offer_obj.second_loan_type == "AFA":
            data_2['Check Box17'] = '/Yes'
        elif buyers_offer_obj.second_loan_type == "Other":
            data_2['Check Box18'] = '/Yes'
            data_1['other type of second loan financing'] = buyers_offer_obj.second_loan_type_other
        
        data_1['second loan fixed rate'] = buyers_offer_obj.second_loan_fixed_rate
        data_1['second loan adjustable rate'] = buyers_offer_obj.second_loan_adjustable_loan_rate
        data_1['shall pay points not to exceed %'] = buyers_offer_obj.second_loan_max_points

    # Escrow Date or Escrow Days
    if buyers_offer_obj.escrow_date:
        data_2['D CLOSE OF ESCROW shall occur on'] = '/On'
    else:
        data_2['dateor'] = '/On'

    # Acknowledgement for form AD
    if buyers_offer_obj.ad:
        data_2['a'] = '/On'

    # If buyer has an agent
    if buyers_offer_obj.buyer_agent:
        # If seller has an agent
        if not buyers_offer_obj.dual_brokerage:
            data_1['Selling Agent'] = buyers_offer_obj.buyer_brokerage_firm
            data_1['Listing Agent'] = buyers_offer_obj.seller_brokerage_firm
            data_2['undefined_2'] = '/On'
            data_2['Listing Agent is the agent of check one'] = '/On'
        else:
            data_1['Listing Agent'] = buyers_offer_obj.buyer_brokerage_firm
            data_2['the Seller exclusively or'] = '/On'

    # Acknowledgement for form PRBS
    if(buyers_offer_obj.prbs):
        data_2['Check Box1'] = '/Yes'

    # Deposit Details
    data_1['initial deposit amount'] = buyers_offer_obj.initial_deposit

    if buyers_offer_obj.deposit_payment_type == "Cashier's Check":
        data_2['Check Box2'] = '/Yes'
    elif buyers_offer_obj.deposit_payment_type == "Personal Check":
        data_2['Check Box3'] = '/Yes'
    elif buyers_offer_obj.deposit_payment_type == "Other":
        data_2['Check Box4'] = '/Yes'
        data_1['other deposit type'] = buyers_offer_obj.deposit_payment_type_other

    # Finance Terms
    if buyers_offer_obj.deposit_due == "Other":
        data_1['agreed upon number of days after acceptance'] = buyers_offer_obj.deposit_due_other

    data_1['additional financing terms 1'] = buyers_offer_obj.additional_terms

    if buyers_offer_obj.down_payment_days != 3:
        data_1['days written verification'] = buyers_offer_obj.down_payment_days

    if buyers_offer_obj.appraisal_contingency:
        data_1['days cancel agreement after acceptance'] = buyers_offer_obj.appraisal_contingency_days
    else:    
        data_2['Check Box21'] = '/Yes'

    data_1['loan application number of days after acceptance'] = buyers_offer_obj.loan_prequalification_days

    if buyers_offer_obj.loan_contingency:
        data_1['loan contigency 21 days or'] = buyers_offer_obj.loan_contingency_days
    
    if buyers_offer_obj.agreement_contingency:
        data_2['no loan contingency'] = '/Yes'

    data_1['other terms page 2'] = buyers_offer_obj.other_terms

    reader = PdfFileReader(application_name + '/static/pdf/' + pdf_name + '.pdf')
    writer = PdfFileWriter()
    set_need_appearances_writer(writer)
    
    for page_number in range(reader.getNumPages()):
        page = reader.getPage(page_number)
        writer.updatePageFormFieldValues(page, data_1)
        tick_buttons(page, data_2)
        writer.addPage(page)

    with open(application_name + '/static/pdf/' + pdf_name + '_filled.pdf',"wb") as pdf:
        writer.write(pdf)