# @author xuluming
# @date 3/24/20 3:40 PM 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helper import selenium_init, get_random_credential
from bdd_tests import access_test, signup_test, signin_test, user_profile_test

driver = selenium_init()

access_test(driver)

# credentials = get_random_credential()
# signup_test(driver, credentials)

credentials = dict(
    email='xuluming95@gmail.com',
    password='xuluming'
)

signin_test(driver, credentials)

user_profile_test(driver)
