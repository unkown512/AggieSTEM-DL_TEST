from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
import re
import time
	
def signup_test(driver: Chrome, credentials: dict):

    username = driver.find_element_by_id('username')
    username.clear()
    username.send_keys(credentials['username'])

    position = driver.find_element_by_id('position')
    select = Select(position)
    select.select_by_value('D')  # D stands for Director option

    phone = driver.find_element_by_id('phone')
    phone.clear()
    phone.send_keys(credentials['phone'])

    password = driver.find_element_by_id('password')
    password.clear()
    password.send_keys(credentials['password'])

    confirm_password = driver.find_element_by_id('conf_password')
    confirm_password.clear()
    confirm_password.send_keys(credentials['password'])

    email = driver.find_element_by_id('email')
    email.clear()
    email.send_keys(credentials['email'])

    confirm_email = driver.find_element_by_id('conf_email')
    confirm_email.clear()
    confirm_email.send_keys(credentials['email'])

    privacy_agreement = driver.find_element_by_id('privacy_agreement')
    select = Select(privacy_agreement)
    select.select_by_value('T')  # T stands for yes

    contact_agreement = driver.find_element_by_id('contact_agreement')
    select = Select(contact_agreement)
    select.select_by_value('T')

    submit = driver.find_element_by_tag_name('button')
    submit.click()
    assert 'signup' not in driver.current_url

def signin_test(driver: Chrome, credentials: dict) -> None:
    email = driver.find_element_by_id('email')
    email.clear()
    email.send_keys(credentials['email'])

    password = driver.find_element_by_id('password')
    password.clear()
    password.send_keys(credentials['password'])

    submit = driver.find_element_by_tag_name('button')
    submit.click()
    assert 'dashboard' in driver.current_url


def dashboard_login_test(driver: Chrome, credentials: dict) -> None:
    target_site = 'http://localhost:5000/dashboard'
    driver.get(target_site)
    button = driver.find_element_by_tag_name('button')
    button.click()

    find = driver.find_element_by_id('login')
    find.click()

    time.sleep(1)
    assert 'user_profile' in driver.current_url
    
    dashboard = driver.find_element_by_xpath("//div[@class='container']/a")
    driver.execute_script("arguments[0].click();",dashboard)
    time.sleep(1)
    assert 'dashboard' in driver.current_url


def dashboard_logout_test(driver: Chrome) -> None:
    target_site = 'http://localhost:5000/dashboard'
    driver.get(target_site)
    button = driver.find_element_by_tag_name('button')
    button.click()

    find = driver.find_element_by_id('logout')
    find.click()
    assert 'signin' in driver.current_url
