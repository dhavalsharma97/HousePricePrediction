from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from datetime import date
from num2words import num2words
import pdfrw
from reportlab.pdfgen import canvas

from buyers_offer.models import BuyersOffer
from sellers_counter_offer.models import SellersCounterOffer


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

    # Data Allocation Details
    if buyers_offer_obj.natural_hazard == 'Buyer':
        data_2['Check Box37'] = '/Yes'

        if buyers_offer_obj.environmental_report:
            data_2['Check Box39'] = '/Yes'

        if buyers_offer_obj.insurance_claim_report:
            data_2['Check Box40'] = '/Yes'
            data_1['hazard disclosure report other payments'] = 'Insurance Claim Report'
            data_1['hazard disclosure report prepared by'] = 'Third Party Vendor'

        if buyers_offer_obj.termite_inspection_report == 'Buyer':
            data_2['Check Box41'] = '/Yes'
            data_1['report 2'] = 'Termite Inspection Report'
            data_1['report 2 prepared by'] = 'Licensed Third Party'
        else:
            data_2['Check Box42'] = '/Yes'
            data_1['report 2'] = 'Termite Inspection Report'
            data_1['report 2 prepared by'] = 'Licensed Third Party'
    else:
        data_2['Check Box38'] = '/Yes'
    
    if buyers_offer_obj.smoke_alarm == 'Buyer':
        data_2['Check Box45'] = '/Yes'
    else:
        data_2['Check Box46'] = '/Yes'

    if buyers_offer_obj.government_inspection == 'Buyer':
        data_2['Check Box47'] = '/Yes'
    else:
        data_2['Check Box48'] = '/Yes'

    if buyers_offer_obj.government_retrofit == 'Buyer':
        data_2['Check Box49'] = '/Yes'
    else:
        data_2['Check Box50'] = '/Yes'

    if buyers_offer_obj.escrow_fee == 'Buyer':
        data_2['Check Box51'] = '/Yes'
    elif buyers_offer_obj.escrow_fee == 'Seller':
        data_2['Check Box52'] = '/Yes'
    else:
        data_2['Check Box51'] = '/Yes'
        data_2['Check Box52'] = '/Yes'
        data_1['buyer/seller shall pay escrow fee'] = 'each to pay their own'

    if buyers_offer_obj.escrow_holder == 'Buyer':
        data_1['escrow holder shall be'] = "Seller's choice"
    else:
        data_1['escrow holder shall be'] = "Buyer's choice"

    data_1['parties shall within number of days'] = buyers_offer_obj.escrow_general_provision

    if buyers_offer_obj.title_insurance == 'Buyer':
        data_2['Check Box53'] = '/Yes'
    else:
        data_2['Check Box54'] = '/Yes'

    data_1['title policy shall be issued by'] = buyers_offer_obj.title_policy

    if buyers_offer_obj.county_transfer == 'Buyer':
        data_2['Check Box55'] = '/Yes'
    else:
        data_2['Check Box56'] = '/Yes'

    if buyers_offer_obj.city_transfer == 'Buyer':
        data_2['Check Box57'] = '/Yes'
    else:
        data_2['Check Box58'] = '/Yes'

    if buyers_offer_obj.hoa_transfer == 'Buyer':
        data_2['Check Box59'] = '/Yes'
    else:
        data_2['Check Box60'] = '/Yes'

    if buyers_offer_obj.hoa_document == 'Buyer':
        data_2['Check Box61'] = '/Yes'
    else:
        data_2['Check Box62'] = '/Yes'

    if buyers_offer_obj.private_transfer == 'Buyer':
        data_2['Check Box63'] = '/Yes'
    else:
        data_2['Check Box64'] = '/Yes'

    if buyers_offer_obj.section_1_termite == 'Buyer':
        data_2['Check Box65'] = '/Yes'
    else:
        data_2['Check Box66'] = '/Yes'
    data_1['other costs 8'] = 'Section 1 Termite Clearance'

    if buyers_offer_obj.tc_fee == 'Buyer':
        data_2['Check Box67'] = '/Yes'
    else:
        data_2['Check Box68'] = '/Yes'
    data_1['other costs 9'] = 'Professional TC Fee'

    if buyers_offer_obj.warranty_waive:
        data_2['Check Box75'] = '/Yes'
    else:
        if buyers_offer_obj.warranty_plan == 'Buyer':
            data_2['Check Box69'] = '/Yes'
        else:
            data_2['Check Box70'] = '/Yes'
        data_1['home warrant not exceed $'] = buyers_offer_obj.warranty_maximal_cost
        
        if buyers_offer_obj.upgraded_warranty:
            data_1['Check Box71'] = '/Yes'

        data_1['home warranty issued by'] = buyers_offer_obj.warranty_company
        
        if buyers_offer_obj.warranty_air_conditioner:
            data_2['Check Box72'] = '/Yes'

        if buyers_offer_obj.warranty_pool_spa:
            data_2['Check Box73'] = '/Yes'

        if buyers_offer_obj.warranty_buyers_choice:
            data_2['Check Box74'] = '/Yes'
            data_2['including other coverages'] = "Buyer's Choice"

    # Item Details
    if buyers_offer_obj.stove:
        data_2['Check Box76'] = '/Yes'
        data_1['all stoves except'] = buyers_offer_obj.exceptions_1
    
    if buyers_offer_obj.refrigerators:
        data_2['Check Box77'] = '/Yes'
        data_1['all refrigerators except'] = buyers_offer_obj.exceptions_2

    if buyers_offer_obj.dryers_washers:
        data_2['Check Box78'] = '/Yes'
        data_1['all washer and dryers except'] = buyers_offer_obj.exceptions_3

    data_1['4 Existing integrated phone and home automation systems including necessary components such as intranet and Internet'] = buyers_offer_obj.additional_items

    if not buyers_offer_obj.phone_automation_system:
        data_2['Check Box79'] = '/Yes'

    data_1['except items and systems identified pursuant to 8B (5)'] = buyers_offer_obj.not_owned_seller
    
    # Closing and Possession Details
    if not buyers_offer_obj.buyer_primary_residence:
        data_2['Check Box81'] = '/Yes'

    data_1['possession delivered time (i)'] = buyers_offer_obj.buyer_possession_1
    
    if buyers_offer_obj.buyer_possession_2:
        data_2['Check Box84'] = '/Yes'
        data_1['possession delivered days'] = buyers_offer_obj.buyer_possession_2

    if buyers_offer_obj.buyer_possession_3:
        data_2['Check Box85'] = '/Yes'
        data_1['posession delivered time (ii)'] = buyers_offer_obj.buyer_possession_3

    if not buyers_offer_obj.property_vacant_2:
        data_1['property vacant days'] = buyers_offer_obj.property_vacant_1
    else:
        data_2['Check Box90'] = '/Yes'

    # Statutory and Disclosure Details
    data_1['condo disclosure days'] = buyers_offer_obj.condominium

    # Time Period Details
    data_1['seller has ______ days'] = buyers_offer_obj.deliver_report

    if buyers_offer_obj.inspection_contingency:
        data_2['Check Box91'] = '/Yes'
        data_1['buyer has ______ days'] = buyers_offer_obj.remove_inspection_contingency

    data_1['number of days access to property'] = buyers_offer_obj.property_access
    data_1['notice to buyer or seller to perform'] = buyers_offer_obj.days_perform
    
    # Verification Details
    data_1['final verification days'] = buyers_offer_obj.final_verification
    
    # Expiration of Offer Details
    data_1['expirate offer time'] = buyers_offer_obj.expiration_time
    data_1['expiration offer date 2'] = buyers_offer_obj.expiration_date
    
    
    reader = PdfFileReader(application_name + '/static/pdf/' + pdf_name + '.pdf')
    writer = PdfFileWriter()
    set_need_appearances_writer(writer)
    
    for page_number in range(reader.getNumPages()):
        page = reader.getPage(page_number)
        writer.updatePageFormFieldValues(page, data_1)
        tick_buttons(page, data_2)
        writer.addPage(page)

    with open(application_name + '/static/pdf/' + pdf_name + '_filled_' + str(buyer_id) + '.pdf',"wb") as pdf:
        writer.write(pdf)


def create_overlay(application_name, pdf_name, seller_id):
    """Create the data that will be overlayed on top of the form that we want to fill"""
    
    c = canvas.Canvas(application_name + '/static/pdf/sellers_counter_offer_temp.pdf')
    c.setFont('Helvetica-BoldOblique', 9)
    c.setFillColor('DarkBlue')

    sellers_counter_offer_obj = SellersCounterOffer.objects.get(pk=seller_id)
    buyers_offer_obj = BuyersOffer.objects.get(pk=sellers_counter_offer_obj.buyers_id)
    
    if not sellers_counter_offer_obj.multiple_offers:
        # Today's Date
        c.drawString(480, 708, str(date.today()))

        # Counter Offer Contract Type
        if sellers_counter_offer_obj.contract_offer == "Purchase Agreement":
            c.drawString(155, 691, 'X')
        elif sellers_counter_offer_obj.contract_offer == "Counter Offer":
            c.drawString(256, 691, 'X')
            c.drawString(365, 692, str(sellers_counter_offer_obj.counter_offer))
        else:
            c.drawString(399, 691, 'X')
            c.drawString(435, 692, sellers_counter_offer_obj.other_contract_offer)

        # Contract Details
        c.drawString(65, 681, str(sellers_counter_offer_obj.contract_sign_date))
        c.drawString(266, 681, sellers_counter_offer_obj.property_address)
        c.drawString(78, 670, sellers_counter_offer_obj.buyers_name)
        c.drawString(56, 659, sellers_counter_offer_obj.sellers_name)
        
        # Offer Price
        if sellers_counter_offer_obj.offer_price_change:
            if sellers_counter_offer_obj.new_offer_price == "Highest And Best Price":
                c.drawString(147, 587, '1. Price to be highest and best price')
            else:
                c.drawString(147, 587, '1. Price to be ' + str(buyers_offer_obj.offer_price))
        else:
            c.drawString(147, 587, '1. Price to be ' + str(buyers_offer_obj.offer_price))
        
        # Company Details
        c.drawString(66, 572, '2. Escrow Company to be ' + sellers_counter_offer_obj.escrow_company_name)
        c.drawString(66, 557, '3. Title Company to be ' + sellers_counter_offer_obj.title_company_name)
        c.drawString(66, 542, '4. Termite Company to be ' + sellers_counter_offer_obj.termite_company_name)
        
        # Other Terms
        if sellers_counter_offer_obj.other_terms:
            c.drawString(66, 527, '5. ' + sellers_counter_offer_obj.other_terms_text)
        
        # Addenda
        if sellers_counter_offer_obj.addenda:
            if sellers_counter_offer_obj.addenda_name_1:
                c.drawString(412, 449, 'X')
                c.drawString(488, 449, 'Addenda')
            elif sellers_counter_offer_obj.addenda_name_2:
                c.drawString(66, 439, 'X')
                c.drawString(78, 439, sellers_counter_offer_obj.addenda_name_2)
            else:
                c.drawString(319, 439, 'X')
                c.drawString(331, 439, sellers_counter_offer_obj.addenda_name_3)

        # Expiration Details
        c.drawString(110, 401, str(sellers_counter_offer_obj.expiration_time))

        if sellers_counter_offer_obj.expiration_meridian == "AM":
            c.drawString(139, 401, 'X')
        else:
            c.drawString(166, 401, 'X')

        c.drawString(205, 401, str(sellers_counter_offer_obj.expiration_date))
    else:
        # Counter Offer Number
        c.drawString(470, 740, '1')

        # Today's Date
        c.drawString(489, 709, str(date.today()))

        # Counter Offer Contract Type
        if sellers_counter_offer_obj.contract_offer == "Other":
            c.drawString(228, 698, 'X')
            c.drawString(263, 699, 'Other')

        # Contract Details
        c.drawString(58, 689, str(sellers_counter_offer_obj.contract_sign_date))
        c.drawString(194, 689, sellers_counter_offer_obj.property_address)
        c.drawString(74, 679, sellers_counter_offer_obj.buyers_name)
        c.drawString(56, 670, sellers_counter_offer_obj.sellers_name)
        
        # Offer Price
        if sellers_counter_offer_obj.offer_price_change:
            if sellers_counter_offer_obj.new_offer_price == "Highest And Best Price":
                c.drawString(136, 604, '1. Price to be highest and best price')
            else:
                c.drawString(136, 604, '1. Price to be ' + str(buyers_offer_obj.offer_price))
        else:
            c.drawString(136, 604, '1. Price to be ' + str(buyers_offer_obj.offer_price))

        # Company Details
        c.drawString(66, 594, '2. Escrow Company to be ' + sellers_counter_offer_obj.escrow_company_name)
        c.drawString(66, 584, '3. Title Company to be ' + sellers_counter_offer_obj.title_company_name)
        c.drawString(66, 575, '4. Termite Company to be ' + sellers_counter_offer_obj.termite_company_name)

        # Other Terms
        if sellers_counter_offer_obj.other_terms:
            c.drawString(66, 566, '5. ' + sellers_counter_offer_obj.other_terms_text)

        # Addenda
        if sellers_counter_offer_obj.addenda:
            if sellers_counter_offer_obj.addenda_name_1:
                c.drawString(359, 527, 'X')
                c.drawString(427, 527, 'Addenda')
            elif sellers_counter_offer_obj.addenda_name_2:    
                c.drawString(65, 518, 'X')
                c.drawString(75, 518, sellers_counter_offer_obj.addenda_name_2)
            else:
                c.drawString(317, 518, 'X')
                c.drawString(328, 518, sellers_counter_offer_obj.addenda_name_3)
        
        # Expiration Details
        c.drawString(51, 442, str(sellers_counter_offer_obj.expiration_time))

        if sellers_counter_offer_obj.expiration_meridian == "AM":
            c.drawString(107, 442, 'X')
        else:
            c.drawString(132, 442, 'X')

        c.drawString(170, 442, str(sellers_counter_offer_obj.expiration_date))

    c.save()


def fill_pdf_1(application_name, pdf_name, seller_id):
    """Merge the specified fillable form PDF with the overlay PDF and save the output"""

    create_overlay(application_name, pdf_name, seller_id)

    form = pdfrw.PdfReader(application_name + '/static/pdf/' + pdf_name + '.pdf')
    olay = pdfrw.PdfReader(application_name + '/static/pdf/sellers_counter_offer_temp.pdf')
    
    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()
        
    writer = pdfrw.PdfWriter()
    writer.write(application_name + '/static/pdf/sellers_counter_offer_filled_' + seller_id + '.pdf', form)