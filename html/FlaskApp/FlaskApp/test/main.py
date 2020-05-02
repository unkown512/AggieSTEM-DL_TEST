from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helper import selenium_init, get_random_credential
from test import access_test, signup_wrong_password_test, signup_short_password_test, signup_wrong_email_test, signup_right_test, signin_test
from test_yuchen import dashboard_login_test, dashboard_logout_test
import random

driver = selenium_init()

access_test(driver)

credentials = dict(
	username= "606"+''.join(random.sample('123456789abcdefg',6)) ,
        phone= ''.join(random.sample('123456789',9)) ,
        email=''.join(random.sample('123456789abcdefg',5)) +"@gmail.com",
        wrong_email='yuchen.jiang0147@outlook.com',
        password= ''.join(random.sample('123456789abcdefg',8)),
        wrong_password='haona1ny30',
        short_password='1234517'
        )

signup_short_password_test(driver, credentials)

signup_right_test(driver, credentials)

signin_test(driver, credentials)

dashboard_login_test(driver, credentials)

dashboard_logout_test(driver)


