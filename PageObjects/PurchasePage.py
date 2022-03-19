from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class PurchasePage:

    country_name = (By.CSS_SELECTOR, "#country")
    countries_list = (By.CSS_SELECTOR, "div[class='suggestions'] ul li a")
    agree_checkbox = (By.CSS_SELECTOR, "div[class*='checkbox checkbox-primary']")
    purchase_button = (By.CSS_SELECTOR, "input[value='Purchase']")
    response_message = (By.CLASS_NAME, "alert-success")


    def __init__(self,parmDriver):
        self.driver = parmDriver

    def get_country_name(self):
        return self.driver.find_element(*PurchasePage.country_name)

    def get_countries_list(self):
        # Define explicit wait for the list of country to popup:
        six_seconds_wait_condition = WebDriverWait(self.driver, 6)  # Explicit wait applicable to certain
        # webDriver command
        # six_seconds_wait_condition.until(expected_conditions.presence_of_all_elements_located(
        #    (By.CSS_SELECTOR, "div[class='suggestions'] ul li a")))
        six_seconds_wait_condition.until(
            expected_conditions.presence_of_all_elements_located(PurchasePage.countries_list))
        return self.driver.find_elements(*PurchasePage.countries_list)

    def get_agree_checkbox(self):
        return self.driver.find_element(*PurchasePage.agree_checkbox)

    def get_purchase_button(self):
        return self.driver.find_element(*PurchasePage.purchase_button)

    def get_response_message(self):
        return self.driver.find_element(*PurchasePage.response_message)
