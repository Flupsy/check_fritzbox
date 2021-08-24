#!/usr/bin/env python

import atexit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


URL = "http://fritzbox.whatever/"
PASSWORD = 'password'

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5)

def close_driver():
    driver.quit()

atexit.register(close_driver)

### Get home page
driver.get(URL)

### Find password field and login button
password = driver.find_element_by_id('uiPass')
login_button = driver.find_element_by_id('submitLoginBtn')

### Fill in password and submit form
password.send_keys(PASSWORD)
login_button.click()

### Find the 'Telephony' menu item and click it to open the menu
### (for some reason click() doesn't work so we do it manually)
try:
    telephony = wait.until(EC.presence_of_element_located((By.ID, 'tel')))
    driver.get(telephony.get_attribute('href'))
except Exception as e:
    print(driver.page_source)
    raise e

### Find 'Telephone Numbers' and click it
try:
    tel_num = wait.until(EC.presence_of_element_located((By.ID, 'myNum')))
    driver.get(tel_num.get_attribute('href'))
except Exception as e:
    print(driver.page_source)
    raise e

### Find the results table and iterate through it
try:
    table = wait.until(EC.visibility_of_element_located((By.ID, 'uiViewFonNumTable')))
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        try:
            row.find_element(By.TAG_NAME, 'th')
        except NoSuchElementException:
            (status, number, connected_via, provider, preselection, _) = row.find_elements(By.TAG_NAME, 'td')
            if 'led_green' in status.get_attribute('class'):
                print(number.get_attribute('innerHTML') + ': ' + 'OK')
            else:
                print(number.get_attribute('innerHTML') + ': ' + 'ERROR')
except Exception as e:
    #print(driver.page_source)
    raise e

