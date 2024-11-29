from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pytest
from test_hrms_login import test_hrms_login  # Ensure this import works correctly


@pytest.fixture
def driver():
    """
    Pytest fixture to set up and tear down the Selenium WebDriver.
    Configures the WebDriver to ignore SSL certificate errors.
    """
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--start-maximized")

    service = Service('C:/Users/mim/pythonProjectall/driver/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()


def test_create_division(driver):
    """
    Test case for creating a division.
    """
    test_hrms_login(driver)

    print("Starting Create Division test.")
    url = "https://amaderit.net/demo/hr/office-division/create"
    driver.get(url)

    print("Navigated to Create Division page.")
    try:
        # Locate the name field and enter division name
        name_field = driver.find_element(By.NAME, "name")
        name_field.send_keys("Test Division")
    except NoSuchElementException:
        raise AssertionError("Test failed: Name field is not available.")

    # Click the Save button
    save_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")
    save_button.click()

    # Wait for toast message and verify
    toast_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='toast-message']"))
    ).text

    assert toast_message == "Division Created Successfully", f"Test Failed: Expected 'Division Created Successfully', but got '{toast_message}'"
    print("Test Passed: Division created successfully.")


def test_edit_division(driver):
    """
    Test case for editing a division.
    """
    test_hrms_login(driver)

    print("Starting Edit Division test.")
    url = "https://amaderit.net/demo/hr/office-division"
    driver.get(url)

    # Click the Edit button for the first division in the list
    edit_button = driver.find_element(By.XPATH, "//tbody/tr[1]/td[2]/a[1]/i[1]")
    edit_button.click()
    print("Navigated to Edit Division page.")

    try:
        # Locate the name field and update the division name
        name_field = driver.find_element(By.NAME, "name")
        name_field.clear()
        name_field.send_keys("Updated Division")
    except NoSuchElementException:
        raise AssertionError("Test failed: Name field is not available.")

    # Click the Update button
    update_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    update_button.click()

    # Wait for toast message and verify
    toast_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='toast-message']"))
    ).text

    assert toast_message == "Division Updated Successfully", f"Test Failed: Expected 'Division Updated Successfully', but got '{toast_message}'"
    print("Test Passed: Division updated successfully.")


def test_delete_division(driver):
    """
    Test case for deleting a division.
    """
    test_hrms_login(driver)

    print("Starting Delete Division test.")
    url = "https://amaderit.net/demo/hr/division"
    driver.get(url)

    # Click the Delete button for the first division in the list
    delete_button = driver.find_element(By.XPATH, "//tbody/tr[1]/td[2]/a[2]/i[1]")
    delete_button.click()

    # Confirm deletion
    confirm_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Yeah, sure!']"))
    )
    confirm_button.click()

    # Wait for toast message and verify
    toast_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='toast-message']"))
    ).text

    assert toast_message == "Division Deleted Successfully", f"Test Failed: Expected 'Division Deleted Successfully', but got '{toast_message}'"
    print("Test Passed: Division deleted successfully.")
