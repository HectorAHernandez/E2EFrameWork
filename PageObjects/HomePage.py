# Home page: Page object definition:
from selenium.webdriver.common.by import By
from PageObjects.CheckoutPage import CheckoutPage


class HomePage:

    # 1- Define one class level object/variable for each webElement object that need to be created, with the
    # corresponding locator
    shop_link = (By.CSS_SELECTOR, "a[href*='shop']")  # this is defining webElement object as a variable object.
    # above from this code in the program: "self.driver.find_element_by_css_selector("a[href*='shop']").click()"

    user_name = (By.NAME, "name")
    email = (By.NAME, "email")
    love_ice_cream_check = (By.ID, "exampleCheck1")
    gender_dropdown_listbox = (By.ID, "exampleFormControlSelect1")
    submit_button = (By.CSS_SELECTOR, "input[type='submit']")
    result_message = (By.CSS_SELECTOR, "[class*='alert-success']")

    # 2- Define a constructor method to receive to driver object from any calling program to any of the getter and
    #    setter methods defined in this page class
    def __init__(self, parm_driver):
        self.driver = parm_driver  # moves the received driver object to a local/instance driver object and make
        # it available to all getter and setter methods defined in this class for each webElement in the page.

    # 3- Created getter and setter methods for each object defined at class level.
    def get_shop_link(self):  # all getter method receive the driver object from the constructor method __init__
        # so that all the webElement objects be available to the getter method.

        # this code was for FW-7:
        # return self.driver.find_element(*HomePage.shop_link)  # the find_element() method can be used to find any of
        # the class level objects/variable, which are reference, in the instance code as className.object/var Name i.e:
        # *HomePage.shopButton, where the '*' is mandatory in order to treat (deserialization) the shopButton object
        # as a tuple containing a list of attributes. If we don't use '*' then it will replace the strings used to
        # defined the shopButton '(By.CSS_SELECTOR, "a[href*='shop']")' as parameter in the find_element() method
        # instead of the deserialized tuple data type. The '*' is needed because we are using a variable object to
        # define a WebElement object and we have to deserialize it.

        # This code is for FW-8:
        # Now the get_shop_link() method click on the link, instantiate the object for the new displayed page and
        # return the driver's object of this new page to the testCase. so we have to remove the click() from testCase.
        self.driver.find_element(*HomePage.shop_link).click()
        checkout_page_object = CheckoutPage(self.driver)
        return checkout_page_object

    def get_user_name(self):
        return self.driver.find_element(*HomePage.user_name)

    def get_email(self):
        return self.driver.find_element(*HomePage.email)

    def get_love_ice_cream_check(self):
        return self.driver.find_element(*HomePage.love_ice_cream_check)

    def get_gender_listbox(self):
        return self.driver.find_element(*HomePage.gender_dropdown_listbox)

    def get_submit_button(self):
        return self.driver.find_element(*HomePage.submit_button)

    def get_result_message(self):
        return self.driver.find_element(*HomePage.result_message)
