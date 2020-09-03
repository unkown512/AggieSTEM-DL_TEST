# @author xuluming
# @date 3/24/20 5:06 PM
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
import re


def access_test(driver: Chrome):
    target_site = 'http://localhost:5000/'
    driver.get(target_site)

    check_string = 'Hello, World! The Aggie STEM DL is currently down due to maintenance.. Please come back another time'
    assert check_string in driver.page_source


def signup_test(driver: Chrome, credentials: dict):
    target_site = 'http://localhost:5000/signup'
    driver.get(target_site)

    username = driver.find_element_by_id('username')
    username.clear()
    username.send_keys(credentials['username'])

    position = driver.find_element_by_id('position')
    select = Select(position)
    select.select_by_value('R')  # R stands for research option

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
    target_site = 'localhost:5000/signin'
    driver.get(target_site)

    email = driver.find_element_by_id('email')
    email.clear()
    email.send_keys(credentials['email'])

    password = driver.find_element_by_id('password')
    password.clear()
    password.send_keys(credentials['password'])

    submit = driver.find_element_by_tag_name('button')
    submit.click()
    assert 'dashboard' in driver.current_url


def search_test(driver: Chrome, search_keywords: str):
    search = driver.find_element_by_id('btn-search')
    search.click()

    keywords = driver.find_element_by_id('keywords')
    keywords.clear()
    keywords.send_keys(search_keywords)

    submit = driver.find_element_by_id('search_keywords')
    submit.click()

    result_table = driver.find_element_by_id('search-result-table')
    rows = result_table.find_elements_by_tag_name('tr')
    for row in rows:
        dataset_name = row.find_elements_by_tag_name('td')[1].text
        # match if found, else assert None
        if row.get_attribute('class') == 'search-result-valid':
            assert re.search(search_keywords, dataset_name, re.IGNORECASE) is not None
        else:
            assert re.search(search_keywords, dataset_name, re.IGNORECASE) is None


def user_profile_test(driver: Chrome) -> None:
    target_site = 'localhost:5000/user_profile'
    driver.get(target_site)
    keywords = 'coco'
    search_test(driver, keywords)
