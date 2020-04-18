# @author xuluming
# @date 3/24/20 3:40 PM 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helper import selenium_init, get_random_credential
from bdd_tests import access_test, signup_test, signin_test, user_profile_test, fill_request_form_test, show_data_test

driver = selenium_init()

access_test(driver)

# credentials = get_random_credential()
# signup_test(driver, credentials)

admin_credential = dict(
    email='xuluming95@gmail.com',
    password='xuluming'
)
user_credential = dict(
    email='xuluming@tamu.edu',
    password='xuluming'
)

signin_test(driver, user_credential)

form_info = dict(
    first_name='Luming',
    last_name='Xu',
    org_name='TAMU',
    phone='9794221234',
    email_address='xuluming@tamu.edu',
    address='College Station TX 77840',
    data_elements='coco',
    research_topics='',
    authors='',
    data_needed='coco',
    start_date='04/02/2020',
    end_date='04/05/2020',
    destroyed_date='04/07/2020'
)
# fill_request_form_test(driver, form_info)
user_profile_test(driver)
# show_data_test(driver)