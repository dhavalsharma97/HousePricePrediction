from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from datetime import date
from num2words import num2words

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
    reader = PdfFileReader(application_name + '/static/pdf/' + pdf_name + '.pdf')
    first_page = reader.getPage(0)

    print(reader.getFields())

    writer = PdfFileWriter()
    set_need_appearances_writer(writer)

    data = {
        'Date Prepared': date.today(),
        'A THIS IS AN OFFER FROM': form_data['first_name'] + ' ' + form_data['last_name'],
        'property to be acquired': form_data['apartment'] + ' ' + form_data['street'],
        'city': form_data['city'],
        'county': form_data['county'],
        'zip code': form_data['zipcode'],
        'purchase price': num2words(form_data['offer_price']),
        'dollars': form_data['offer_price']
    }

    # Check Box - /Yes
    # Button - /On
    if (form_data['down_payment'] != -1):
        data['BALANCE OF DOWN PAYMENT OR PURCHASE PRICE in the amount of'] = form_data['down_payment']
    else:    
        tick_buttons(first_page, {'Check Box6': '/Yes'})

    writer.updatePageFormFieldValues(first_page, data)
    writer.addPage(first_page)

    with open(application_name + '/static/pdf/' + pdf_name + '_filled.pdf',"wb") as new:
        writer.write(new)

"""fill_pdf('buyers_offer', 'purchase_agreement', {
    'first_name': 'Dhaval',
    'last_name': 'Sharma',
    'offer_price': 250000,
    'apartment': '6621',
    'street': 'Montezuma Rd',
    'city': 'San Diego',
    'county': 'San Diego',
    'zipcode': 92115,
    'down_payment': 50000
})"""