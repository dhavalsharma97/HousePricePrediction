import pdfrw
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from datetime import date
from num2words import num2words
import PyPDF2 as pypdf

def create_overlay():
    """Create the data that will be overlayed on top of the form that we want to fill"""
    
    c = canvas.Canvas('helpers/purchase_agreement_1.pdf')
    c.setFontSize(10)

    c.drawString(102, 691, '01/31/2021')
    c.drawString(173, 673, 'Dhaval Sharma')
    c.drawString(231, 661, 'Hello')
    c.drawString(66, 651, 'Hello')
    c.drawString(181, 651, 'Hello')
    c.drawString(314, 651, 'Hello')
    c.drawString(446, 631, 'Hello')
    c.drawString(66, 340, 'Hello')

    c.save()

def merge_pdfs(form_pdf, overlay_pdf, output):
    """Merge the specified fillable form PDF with the overlay PDF and save the output"""

    form = pdfrw.PdfReader(form_pdf)
    olay = pdfrw.PdfReader(overlay_pdf)
    
    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()
        
    writer = pdfrw.PdfWriter()
    writer.write(output, form)

#create_overlay()
#merge_pdfs('helpers/purchase_agreement.pdf', 'helpers/purchase_agreement_1.pdf', 'helpers/final_purchase_agreement.pdf')


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
                    NameObject("/V"): NameObject(fields[field]),
                    NameObject("/AS"): NameObject(fields[field])
                })

def fill_pdf(application_name, pdf_name, form_data):
    reader = PdfFileReader(pdf_name + '.pdf')
    first_page = reader.getPage(1)

    print(reader.getFields())

    writer = PdfFileWriter()
    set_need_appearances_writer(writer)

    data_1 = {
        'Date Prepared': date.today(),
        'A THIS IS AN OFFER FROM': form_data['first_name'] + ' ' + form_data['last_name'],
        'property to be acquired': form_data['apartment'] + ' ' + form_data['street'],
        'city': form_data['city'],
        'county': form_data['county'],
        'zip code': form_data['zipcode'],
        'purchase price': num2words(form_data['offer_price']),
        'dollars': form_data['offer_price'],
        'parcel number': form_data['parcel_number'],
        'buyer deposit made payable to': form_data['escrow_date'],
        'E Buyer and Seller are referred to herein as the Parties Brokers are not Parties to this Agreement': form_data['escrow_days'],
        'Listing Agent': 'Hello'
    }

    # Check Box - /Yes
    # Button - /On
    if (form_data['down_payment'] != -1):
        data_1['BALANCE OF DOWN PAYMENT OR PURCHASE PRICE in the amount of'] = form_data['down_payment']
    else:    
        tick_buttons(first_page, {'Check Box6': '/Yes'})
    
    data_2 = {
        'D CLOSE OF ESCROW shall occur on': '/On',
        'dateor': '/On'
    }

    data_2['Check Box7'] = '/Yes'
    data_1['all cash offer number of days'] = 'Test'
    data_1['second load amount'] = 'Test'
    data_1['loan application number of days after acceptance'] = '/Yes'
    data_1['other terms page 2'] = 'Test'
    
    data_2['Check Box1'] = '/Yes'
    data_2['undefined_2'] = '/On'
    data_2['the Seller exclusively or'] = '/On'
    data_2['Listing Agent is the agent of check one'] = '/On'
    data_2['the Buyer exclusively or'] = '/On'
    data_2['the Seller exclusively or_2'] = '/On'

    tick_buttons(first_page, data_2)

    writer.updatePageFormFieldValues(first_page, data_1)
    writer.addPage(first_page)

    for j in range(0, len(first_page['/Annots'])):
        print(first_page['/Annots'][j].getObject())

    with open(pdf_name + '_filled.pdf',"wb") as new:
        writer.write(new)

fill_pdf('buyers_offer', 'purchase_agreement', {
    'first_name': 'Dhaval',
    'last_name': 'Sharma',
    'offer_price': 250000,
    'apartment': '6621',
    'street': 'Montezuma Rd',
    'city': 'San Diego',
    'county': 'San Diego',
    'zipcode': 92115,
    'down_payment': 50000,
    'parcel_number': '111-111-1111',
    'escrow_date': date.today(),
    'escrow_days': '25'
})


pdfobject=open('purchase_agreement_filled.pdf','rb')
pdf=pypdf.PdfFileReader(pdfobject)
print()
print(pdf.getFormTextFields())
