from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helper import selenium_init, get_random_credential
from test_access_level import signup_test, signin_test, dashboard_logout_test, test_change_access, admin_signin_test, admin_dashboard_manage_users_test 
import random

driver = selenium_init()

credentials = dict(
	username="606"+''.join(random.sample('123456789abcdefg',6)),
	phone=''.join(random.sample('123456789',9)),
    email=''.join(random.sample('123456789abcdefg',5)) + "@gmail.com",
    password=''.join(random.sample('123456789abcdefg',8))
)

signup_test(driver, credentials)

signin_test(driver, credentials)

dashboard_logout_test(driver)

test_change_access()

admin_signin_test(driver, credentials)

admin_dashboard_manage_users_test(driver)
