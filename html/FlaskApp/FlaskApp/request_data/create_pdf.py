# simple_demo.py
from fpdf import FPDF
import time


def create_form(data, path):
    pdf = FPDF('P', 'mm', format='A4')
    pdf.add_page('P')
    pdf.set_font('Times', 'B', size=24)
    pdf.cell(0, 15, txt="Aggie STEM Data Request", ln=1, align="C")

    requestor_information(data, pdf)
    requested_data_elements(data, pdf)
    data_usage(data, pdf)
    data_access_details(data, pdf)

    pdf.output(path)


def requestor_information(data, pdf):
    """
    Print Requestor Information
    """

    pdf.set_font('Arial', 'B', size=12)
    prev_y = pdf.y
    pdf.multi_cell(0, 5, ('Issued on: %s' % str(time.strftime("%d-%m-%Y"))))
    pdf.x = pdf.x + 70
    pdf.y = prev_y
    pdf.multi_cell(0, 5, ('Data Period: %s - %s' % (data['start_date'], data['end_date'])))
    prev_y = pdf.y
    pdf.multi_cell(0, 5, ('Data Needed By: %s' % data['needed_date']))
    pdf.x = pdf.x + 70
    pdf.y = prev_y
    pdf.multi_cell(0, 5, ('Destroyed Date: %s' % data['destroyed_date']))
    pdf.multi_cell(0, 15, 'Requestor Information')

    pdf.set_font('Arial', size=12)
    pdf.multi_cell(0, 0, ('Name: %s, %s' % (data['first_name'], data['last_name'])))
    left_x = pdf.x
    left_y = pdf.y
    pdf.multi_cell(0, 0, ('Organization: %s' % data['org_name']), 0, 'R')
    pdf.y = pdf.y + 5
    pdf.multi_cell(0, 0, ('Status: %s' % data['status']), 0, 'R')
    pdf.y = pdf.y + 5
    pdf.multi_cell(0, 0, ('Address: %s' % data['address']), 0, 'R')

    pdf.x = left_x
    pdf.y = left_y

    pdf.multi_cell(0, 10, ('Phone Number: %s' % data['phone']))
    pdf.multi_cell(0, 0, ('Email: %s' % data['email_address']))


def requested_data_elements(data, pdf):
    """
    Print Requested Data Elements
    """
    pdf.y = pdf.y + 5
    pdf.set_font('Arial', 'B', size=12)
    pdf.multi_cell(0, 15, 'Requested Data Elements')
    pdf.set_font('Arial', size=12)

    pdf.multi_cell(0, 0, data['data_elements'])


def data_usage(data, pdf):
    """
    Print Data usage
    """
    pdf.y = pdf.y + 5
    pdf.set_font('Arial', 'B', size=12)
    pdf.multi_cell(0, 15, 'Data Usage')
    pdf.set_font('Arial', 'B', size=10)
    pdf.multi_cell(0, 5, "Topic of your research and research questions")
    pdf.set_font('Arial', size=10)
    txt_wrapper(data['research_topics'], pdf)

    # List co-researchers and authors ...
    pdf.set_font('Arial', 'B', size=10)
    pdf.multi_cell(0, 5, "co-researchers and authors")
    pdf.set_font('Arial', size=10)
    txt_wrapper(data['authors'], pdf)

    # Please DESCRIBE IN DETAIL the data ...
    pdf.set_font('Arial', 'B', size=10)
    pdf.multi_cell(0, 5, "Data Needed from Aggie STEM")
    pdf.set_font('Arial', size=10)
    txt_wrapper(data['data_needed'], pdf)

    # Please DESCRIBE IN DETAIL how the data ...
    pdf.set_font('Arial', 'B', size=10)
    pdf.multi_cell(0, 5, "How the data will be used")
    pdf.set_font('Arial', size=10)
    txt_wrapper(data['data_how'], pdf)


def data_access_details(data, pdf):
    """
    Print Data Access Details
    """
    pdf.y = pdf.y + 5
    pdf.set_font('Arial', 'B', size=12)
    pdf.multi_cell(0, 15, 'Data Access Details')

    # Who will have accesss ....
    pdf.set_font('Arial', 'B', size=10)
    pdf.multi_cell(0, 10, "Who will have access to the requested data?")
    pdf.set_font('Arial', size=10)

    pdf.multi_cell(0, 0, ('Name: %s' % data['data_details1_name']))
    left_y = pdf.y
    pdf.multi_cell(0, 0, ('Institution: %s' % data['data_details1_inst']), 0, 'R')
    pdf.y = pdf.y + 5
    pdf.multi_cell(0, 0, ('Phone: %s' % data['data_details1_phone']), 0, 'R')
    pdf.y = left_y + 5
    pdf.multi_cell(0, 0, ('Email: %s' % data['data_details1_email']))

    # Who will be responsible ....
    pdf.set_font('Arial', 'B', size=10)
    pdf.multi_cell(0, 10, "Who will be directly responsible for the security of the data?")
    pdf.set_font('Arial', size=10)

    pdf.multi_cell(0, 0, ('Name: %s' % data['data_details2_name']))
    left_y = pdf.y
    pdf.multi_cell(0, 0, ('Institution: %s' % data['data_details2_inst']), 0, 'R')
    pdf.y = pdf.y + 5
    pdf.multi_cell(0, 0, ('Phone: %s' % data['data_details2_phone']), 0, 'R')
    pdf.y = left_y + 5
    pdf.multi_cell(0, 0, ('Email: %s' % data['data_details2_email']))

    # Data storage ...
    pdf.y = pdf.y + 5
    pdf.set_font('Arial', 'B', size=10)
    pdf.multi_cell(0, 5, "Data Storage")
    pdf.set_font('Arial', size=10)
    txt_wrapper(data['data_storage'], pdf)


def txt_wrapper(msg, pdf):
    length = 0
    txt = ""
    for char in msg:
        if (length == 140):
            pdf.multi_cell(0, 5, txt)
            txt = ""
            length = 0
        txt += char
        length += 1
    if (txt != ""):
        pdf.multi_cell(0, 5, txt)
