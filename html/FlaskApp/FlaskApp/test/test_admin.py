from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
import re
import time


def signin_test(driver: Chrome, credentials: dict) -> None:
    target_site = 'http://localhost:5000/signin'
    driver.get(target_site)

    email = driver.find_element_by_id('email')
    email.clear()
    email.send_keys(credentials['email'])

    password = driver.find_element_by_id('password')
    password.clear()
    password.send_keys(credentials['password'])

    submit = driver.find_element_by_tag_name('button')
    submit.click()

    time.sleep(1)
    assert 'dashboard' in driver.current_url


def dashboard_manage_users_test(driver: Chrome) -> None:  
    target_site = 'http://localhost:5000/dashboard'
    driver.get(target_site)
    
    button = driver.find_element_by_tag_name('button')	
    button.click()
    
    find = driver.find_element_by_id('manageuser')
    find.click()

    time.sleep(1)
    assert 'manage_users' in driver.current_url
    

def dashboard_manage_data_access_test(driver: Chrome) -> None:	
    target_site = 'http://localhost:5000/dashboard'
    driver.get(target_site)
    
    button = driver.find_element_by_tag_name('button')
    button.click()

    find = driver.find_element_by_id('manage-data-access')
    find.click()

    time.sleep(1)
    assert 'manage_data_access' in driver.current_url


def dashboard_message_users_test(driver: Chrome) -> None:
    target_site = 'http://localhost:5000/dashboard'
    driver.get(target_site)

    button = driver.find_element_by_tag_name('button')
    button.click()
    
    find = driver.find_element_by_id('messageusers')
    find.click()

    time.sleep(1)
    assert 'message_users' in driver.current_url
    
    dashboard = driver.find_element_by_xpath("//div[@class='container']/a")
    driver.execute_script("arguments[0].click();", dashboard)
    assert 'dashboard' in driver.current_url
    



