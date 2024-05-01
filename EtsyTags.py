import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
with open('secrets.txt') as file:
    for line in file:
        key, value = line.strip().split('=')
        os.environ[key] = value
DELAY = random.uniform(0.1, 0.3)
LISTING_URL = 'https://www.etsy.com/your/shops/PrintGeekStaging/tools/listings'


def login_etsy() -> webdriver.Chrome:
    """ Logs into etsy for tagging """
    driver: webdriver.Chrome = webdriver.Chrome()
    driver.get(LISTING_URL)
    email_input = driver.find_element(By.ID, 'join_neu_email_field')
    email: str = os.environ.get('EMAIL')
    for char in email:
        email_input.send_keys(char)
        time.sleep(DELAY)
    pass_input = driver.find_element(By.ID, 'join_neu_password_field')
    password: str = os.environ.get('PASSWORD')
    for char in password:
        pass_input.send_keys(char)
        time.sleep(DELAY)
    login_button = driver.find_element(By.NAME, 'submit_attempt')
    login_button.click()
    time.sleep(30)
    return driver


def update_tags(driver: webdriver.Chrome, title: str, tags: list[str]) -> None:
    """ Updates tags on an individual listing """
    driver.get(LISTING_URL)
    listing_title = driver.find_element(By.XPATH, f'//h2[text()="{title}"]')
    listing_title.click()
    time.sleep(5)
    listing_tags_input = driver.find_element(By.ID, 'listing-tags-input')
    for tag in tags:
        for char in tag:
            listing_tags_input.send_keys(char)
            time.sleep(DELAY)
        listing_tags_input.send_keys(Keys.ENTER)
        time.sleep(0.8)
    publish_button = driver.find_element(By.XPATH, '//button[@data-test="publish"]')
    publish_button.click()
    time.sleep(2)
    return


def close_driver(driver: webdriver.Chrome) -> None:
    driver.quit()
    print('Tagging Finished')
    return
