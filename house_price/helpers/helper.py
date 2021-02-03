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
                    NameObject('/V'): NameObject(fields[field]),
                    NameObject('/AS'): NameObject(fields[field])
                })

def fill_pdf(application_name, pdf_name, form_data):
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
        'E Buyer and Seller are referred to herein as the Parties Brokers are not Parties to this Agreement': form_data['escrow_days']
    }

    # Check Box - /Yes
    # Button - /On
    data_2 = {
        'D CLOSE OF ESCROW shall occur on': '/On',
        'dateor': '/On'
    }

    reader = PdfFileReader(application_name + '/static/pdf/' + pdf_name + '.pdf')
    writer = PdfFileWriter()
    set_need_appearances_writer(writer)
    
    for page_number in range(reader.getNumPages()):
        page = reader.getPage(page_number)

        if (form_data['down_payment'] != -1):
            data_1['BALANCE OF DOWN PAYMENT OR PURCHASE PRICE in the amount of'] = form_data['down_payment']
        else:    
            tick_buttons(page, {'Check Box6': '/Yes'})

        writer.updatePageFormFieldValues(page, data_1)
        tick_buttons(page, data_2)

        writer.addPage(page)

    with open(application_name + '/static/pdf/' + pdf_name + '_filled.pdf',"wb") as pdf:
        writer.write(pdf)