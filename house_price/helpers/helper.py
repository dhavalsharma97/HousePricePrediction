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

    # Is the payment Cash or Loan
    if (buyers_offer_obj.down_payment != -1):
        data_1['BALANCE OF DOWN PAYMENT OR PURCHASE PRICE in the amount of'] = buyers_offer_obj.down_payment
    else:    
        data_2['Check Box6'] = '/Yes'

    # Escrow Date or Escrow Days
    if(buyers_offer_obj.escrow_date):
        data_2['D CLOSE OF ESCROW shall occur on'] = '/On'
    else:
        data_2['dateor'] = '/On'

    # Acknowledgement for form AD
    if(buyers_offer_obj.ad):
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