from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pytest
from test_hrms_login import test_hrms_login  # Ensure this import works correctly


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



def test_create_bank(driver):
    """Test case for creating a new bank."""
    test_hrms_login(driver)

    print("Starting Create Bank test.")
    url = "https://amaderit.net/demo/hr/bank/create"
    driver.get(url)
    print("Navigated to Create Bank page.")

    try:
        # Locate and interact with the name field
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )
        name_field.send_keys("Nurunnahar")
        print("Entered bank name: 'Bank of nur'.")

        # Locate and click the save button
        save_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")
        save_button.click()

        # Wait for and validate the toast message
        toast_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='toast-message']"))
        ).text
        assert toast_message == "Bank Created Successfully", \
            f"Test Failed: Expected 'Bank Created Successfully', but got '{toast_message}'."
        print("Test Passed: Bank creation was successful.")
    except (NoSuchElementException, TimeoutException) as e:
        raise AssertionError(f"Test failed: {str(e)}")


def test_edit_bank(driver):
    """Test case for editing an existing bank."""
    test_hrms_login(driver)

    print("Starting Edit Bank test.")
    url = "https://amaderit.net/demo/hr/bank"
    driver.get(url)
    print("Navigated to Bank List page.")

    try:
        # Locate and click the edit button for the desired row
        edit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[2]/a[1]/i[1]"))
        )
        edit_button.click()
        print("Clicked Edit button.")

        # Update the name field
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )
        name_field.clear()
        name_field.send_keys("Chase Bank")
        print("Updated name to 'Chase Bank'.")

        # Submit the update
        update_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        update_button.click()

        # Validate the toast message
        toast_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='toast-message']"))
        ).text
        assert toast_message == "Bank Updated Successfully", \
            f"Test Failed: Expected 'Bank Updated Successfully', but got '{toast_message}'."
        print("Test Passed: Bank updated successfully.")
    except (NoSuchElementException, TimeoutException) as e:
        raise AssertionError(f"Test failed: {str(e)}")


def test_delete_bank(driver):
    """Test case for deleting a bank."""
    test_hrms_login(driver)

    print("Starting Delete Bank test.")
    url = "https://amaderit.net/demo/hr/bank"
    driver.get(url)
    print("Navigated to Bank List page.")

    try:
        # Locate and click the delete button for the first row
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[2]/a[2]/i[1]"))
        )
        delete_button.click()
        print("Clicked Delete button.")

        # Confirm the delete action
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yeah, sure!']"))
        )
        confirm_button.click()

        # Optionally, validate if the row is removed or a toast message
        toast_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='toast-message']"))
        ).text
        assert "Deleted" in toast_message, \
            f"Test Failed: Expected a delete confirmation message, but got '{toast_message}'."
        print("Test Passed: Bank deleted successfully.")
    except (NoSuchElementException, TimeoutException) as e:
        raise AssertionError(f"Test failed: {str(e)}")
