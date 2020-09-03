from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helper import selenium_init, get_random_credential
from test_admin import signin_test, dashboard_manage_users_test, dashboard_manage_data_access_test, dashboard_message_users_test
from test_yuchen import dashboard_logout_test


driver = selenium_init()

# credentials = get_random_credential()
# signup_test(driver, credentials)

credentials = dict(
    email='1312175346@qq.com',
    password='zxcvbnm142857'
)

signin_test(driver, credentials)

dashboard_manage_users_test(driver)

dashboard_manage_data_access_test(driver)

dashboard_message_users_test(driver)

dashboard_logout_test(driver)
