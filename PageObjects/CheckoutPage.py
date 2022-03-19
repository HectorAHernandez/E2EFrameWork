# Checkout page: Page object definition:
from selenium.webdriver.common.by import By

from PageObjects.PurchasePage import PurchasePage


class CheckoutPage:

    # 1- Define one class level object/variable for each webElement object that need to be created, with the
    # corresponding locator
    product_name_list = (By.CSS_SELECTOR, "div[class='card h-100'] div h4 a")
    add_to_cart_button = (By.CSS_SELECTOR, "div[class='card h-100'] div button")
    checkout_button = (By.CSS_SELECTOR, "a[class*='btn-primary']")
    product_in_shopping_cart_list = (By.XPATH, "//tbody/tr")
    product_in_shopping_cart_name = (By.XPATH, "//td[1]/div[@class='media']/div/h4/a")
    product_in_shopping_cart_quantity = (By.CSS_SELECTOR, "td input")
    product_in_shopping_cart_price = (By.XPATH, "//td[3]/strong")
    product_in_shopping_cart_total = (By.XPATH, "//td[4]/strong")
    final_checkout_buttton = (By.CSS_SELECTOR, "button[class*='btn-succe")

    # 2- Define a constructor method to receive to driver object from any calling program to any of the getter and
    #    setter methods defined in this page class
    def __init__(self, parm_driver):
        self.driver = parm_driver  # moves the received driver object to a local/instance driver object and make
        # it available to all getter and setter methods defined in this class for each webElement in the page.

    # 3- Created getter and setter methods for each object defined at class level.
    # Example from previous page HomePage:
    # def get_shop_link(self):  # all getter method receive the driver object from the constructor method __init__
        # so that all the webElement objects be available to the getter method.

        # return self.driver.find_element(*HomePage.shop_link)  # the find_element() method can be used to find any of
        # the class level objects/variable, which are reference, in the instance code as className.object/var Name i.e:
        # *HomePage.shopButton, where the '*' is mandatory in order to treat (deserialization) the shopButton object
        # as a tuple containing a list of attributes. If we don't use '*' then it will replace the strings used to
        # defined the shopButton '(By.CSS_SELECTOR, "a[href*='shop']")' as parameter in the find_element() method
        # instead of the deserialized tuple data type. The '*' is needed because we are using a variable object to
        # define a WebElement object and we have to deserialize it.

    def get_product_names_list(self):
        return self.driver.find_elements(*CheckoutPage.product_name_list)

    def get_add_to_cart_buttons_list(self):
        return self.driver.find_elements(*CheckoutPage.add_to_cart_button)

    def get_checkout_button(self):
        return self.driver.find_element(*CheckoutPage.checkout_button)

    def get_products_in_shopping_cart_list(self):
        return self.driver.find_elements(*CheckoutPage.product_in_shopping_cart_list)

    def get_product_in_shopping_cart_name(self):
        return self.driver.find_element(*CheckoutPage.product_in_shopping_cart_name)

    def get_product_in_shopping_cart_quantity(self):
        return self.driver.find_element(*CheckoutPage.product_in_shopping_cart_quantity)

    def get_product_in_shopping_cart_price(self):
        return self.driver.find_element(*CheckoutPage.product_in_shopping_cart_price)

    def get_product_in_shopping_cart_total(self):
        return self.driver.find_element(*CheckoutPage.product_in_shopping_cart_total)

    def get_final_checkout_button_click(self):
        # This code is for FW-8:
        # Now the final_checkout_butttonk() method click on the link, instantiate the object for the new displayed page and
        # return the driver's object of this new page to the testCase. so we have to remove the click() from testCase.
        self.driver.find_element(*CheckoutPage.final_checkout_buttton).click()
        purchase_page_object = PurchasePage(self.driver)
        return purchase_page_object
