from telnetlib import EC

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from test_hrms_login import test_hrms_login

from test_login import test_login

from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture
def driver():
    """
    Pytest fixture to set up and tear down the Selenium WebDriver.
    Configures the WebDriver to ignore SSL certificate errors.
    """
    # Set up Chrome options to handle SSL certificate issues
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--start-maximized")  # Maximize the browser

    # Set up the WebDriver service
    service = Service('C:/Users/mim/pythonProjectall/driver/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver  # Provide the WebDriver to the test
    driver.quit()  # Ensure the browser is closed after the test


def test_create_address(driver):

    test_hrms_login(driver)

    print("Starting Create Address test.")
    url = "https://amaderit.net/demo/hr/division/create"
    driver.get(url)

    print("Navigated to Create Address page.")

    try:
        # Locate and interact with the name fields
        name_field = driver.find_element(By.NAME, "name")
    except NoSuchElementException:
        raise AssertionError("Test failed: Username or password field is not available.")

    # Enter the login credentials
    name_field.send_keys("Dubai")


    # Locate and click the login button
    create_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")
    create_button.click()

    WebDriverWait(driver, 6)

    #  Get the text of the toast message
    toast_message = driver.find_element(By.XPATH, "//div[@class='toast-message']").text

    # Assert that the message is "Division Created Successfully"
    if toast_message == "Division Created Successfully":
        print("Test Passed: Division creation was successful.")
    else:
        assert False, f"Test Failed: Expected 'Division Created Successfully', but got"


def test_delete_address(driver):
    test_hrms_login(driver)

    print("Starting Delete Address test.")
    url = "https://amaderit.net/demo/hr/division"
    driver.get(url)

    print("Navigated to Address List page.")

    # Locate and click the login button
    delete_button = driver.find_element(By.XPATH, "//tbody/tr[1]/td[2]/a[2]/i[1]")
    delete_button.click()
    WebDriverWait(driver, 5)
    delete_yes_button = driver.find_element(By.XPATH, "//button[normalize-space()='Yeah, sure!']")
    delete_yes_button.click()
    WebDriverWait(driver, 5)
    print("Delete List")

def test_edit_address(driver):

    test_hrms_login(driver)

    print("Starting Edit Address test.")
    url = "https://amaderit.net/demo/hr/division"
    driver.get(url)

    edit_button = driver.find_element(By.XPATH, "//tbody/tr[6]/td[2]/a[1]/i[1]")
    edit_button.click()
    print("Clicked Edit Btn")

    try:
        # Locate and interact with the name fields
        name_field = driver.find_element(By.NAME, "name")
    except NoSuchElementException:
        raise AssertionError("Test failed: Username or password field is not available.")

    # Enter the login credentials
    name_field.send_keys("Abu dhabi")


    # Locate and click the update button
    update_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    update_button.click()


    #  Get the text of the toast message
    toast_message = driver.find_element(By.XPATH, "//div[@class='toast-message']").text

    # Assert that the message is "Division Created Successfully"
    if toast_message == "Division Updated Successfully":
        print("Test Passed: Division Updated Successfully.")
    else:
        assert False, f"Test Failed: Expected 'Division Updated Successfully"





