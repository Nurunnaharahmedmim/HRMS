import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Pytest fixture to handle WebDriver setup and teardown
@pytest.fixture
def driver():
    # Set up Chrome options to bypass SSL errors
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--incognito")

    # Set up the WebDriver
    service = Service('C:/Users/mim/pythonProjectall/driver/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver


    driver.quit()


def test_hrms_login(driver):
    """Test case for HRMS login with SSL bypass."""
    # Navigate to the HRMS login page
    hrms_url = "https://amaderit.net/demo/hr/login"
    driver.get(hrms_url)
    logging.info("Navigated to HRMS login page.")

    try:
        # Locate the username and password fields
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        # Enter login credentials
        username_field.send_keys("12345678")
        password_field.send_keys("12345678")

        # Locate and click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sign In']"))
        )
        login_button.click()
        logging.info("Clicked the sign-in button.")

        # # Validate successful login by checking for a dashboard element
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "Dashboard"))
        # )
        # logging.info("Login successful. Dashboard loaded.")
        #
        # # Assert the current URL indicates successful login
        # assert "dashboard" in driver.current_url.lower(), "Login successful, but dashboard URL not loaded."

    except Exception as e:
        logging.error(f"Login test failed: {e}")
        pytest.fail("HRMS login test failed due to an exception.")
