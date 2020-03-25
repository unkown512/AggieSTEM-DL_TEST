# @author xuluming
# @date 3/24/20 3:42 PM 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
from datetime import datetime


def get_current_path():
    return os.path.dirname(os.path.abspath(__file__))


def selenium_init():
    chrome_options = Options()
    driver = webdriver.Chrome(executable_path=get_current_path() + '/chromedriver',
                              options=chrome_options)
    driver.implicitly_wait(6)  # wait if element not found
    return driver


def get_random_credential():
    # unique email and phone number
    # name in "First Last" format

    t = str(datetime.now()).split(' ')
    username = t[1].replace(':', '').replace('.', '')
    password = username
    phone = password
    email = username + '@qq.com'
    credentials = dict(
        username=username,
        password=password,
        email=email,
        phone=phone
    )
    return credentials
