# This is the first program for the functional End To End test.
# This program:
# 1- Click on the Shop Link.
# 2- Click on the Shopping cart button to add a product to the shopping cart
# 3- Click on the Checkout button to go to the shopping cart
# 4- validate the product in the shopping cart
# 5- if selected product is in the shopping cart then click on the Checkout button.
# 6- type the delivery country location
# 7- to select the country:
# 8- Define explicit wait for the list of country to popup:
# 9- after list of country popped up, create countriesList
# 10- loop the countriesList to click the desired country:
# 11- click on the 'I agree' checkbox
# 12- Click on the Purchase button:
# 13- to grab the value in the response message displayed, which is NOT a real alert that we can switch_to:
# 14- now we can use Selenium to take a screenshot of the page with the successful message.

# this program is based in the P15EnToEnd_01.py and we are going to convert it into a pyTest.py type,
# which means encapsulate it into a class and "def methodName(self: ..."
# Below the steps taken to convert the program to the standard used by the Framework coding.
# FW-1: Move all the webDriver settings, opening the URL and maximize to a fixture in the conftest.py file, because
#       the fixture runs at class level before any testCase execution.
# FW-2: Connect the driver object in the program with the new definition of the webDriver in the conftest.py file, now
#       because the 'yield' and 'return' command cannot be together in the conftest.py file we have change the
#       'returm driver' command by 'request.cls.driver = driver' after completed this now we change all the references
#       to the 'driver' object to now call the 'setup' fixture's class-level variable 'driver' by using the
#       'self.driver' (inheriting a class-level variable/object from the parent class ('setup'))
# FW-3  In this pyTest.py program/script, if we have 10 classes we would need to invoke the 'setup' fixture 10 times
#       (@pytest.mark.usefixtures("setup")), so to make this program more Framework efficient we can create a
#       BaseClassUtilities/utilities class where we invoke the 'setup' fixture once and then by inheriting this
#       BaseClassUtilities all others child class can make use of this 'setup' fixture. So all driver's setting and
#       any other common code is ONLY placed in this BaseClassUtilities. And then removed the 'setup'
#       fixture invocation statement (@pytest.mark.usefixtures("setup")) from this program.
#       For this BaseClass we created the 'utilities' Python package and created this BaseClass in it.

# FW-4  Prepare the Framework to handle/receive command prompt commands, i.e. the browser_name that we would like to
#       execute the test at any given moment, by adding the flag '--browser_name firefox' in the execution command:
#       py.test test_01SelectProductAndPurchase.py -v -s --browser_name firefox
#       this webpage contains example of how to define the command prompt flags/hooks for pyTest:
#       https://docs.pytest.org/en/6.2.x/example/simple.html. see the conftest.py for detail on how it was implemented.
# FW-6  continue in program test_02PageObjectSelectProductPurchase.py
# FW-7
# FW-8
# FW-9
# FW-10
# FW-11
# FW-12


from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utilities.BaseClassUtilities import BaseClassUtilities

# @pytest.mark.usefixtures("setup")    commented to be eliminated, because now we are using the BaseClassUtilities,
# which contains the 'setup' fixture invocation and any other general use utility code. Because now, by inheritance,
# this TestEndtoEndShop class, has access or knowledge of the 'setup' fixture and don't need to invoke it by itself


class TestEndToEndShop(BaseClassUtilities):

    def test_select_product_and_purchase(self):   # setup was eliminated because with 'self' we have now access to
        # all the code in the parent class BaseClassUtilities, including the 'setup' fixture.
        # def test_select_product_and_purchase(self, setup):

        # initialize product_to_select:
        product_to_select = "nokia"
        product_found = False
        name_product_in_sc = ""

        # click on the Shop link.
        self.driver.find_element_by_css_selector("a[href*='shop']").click()

        # 1: Build a list of all the products displayed:
        products_list = self.driver.find_elements_by_css_selector("div[class='card h-100']")  # or
        # //div[@class='card h-100']

        for productItem in products_list:
            print("Whole product Object in List:", productItem.text)

            # product contains the CSS path for the iterated productItem "div[class='card h-100']" as a parent
            # and now we have access to the CSS selector or Xpath of the children by using the productItem object
            product_name = productItem.find_element_by_css_selector("div h4 a").text  # "div h4 a" OR "div/h4/a"
            # instead of the whole path "div[class ='card h-100'] h4 a" OR //div[@class='card h-100']/div/h4/a"
            # because productItem points to the parent part of the path.
            # Note: in the Xpath DO NOT start with '//', as normal, because it will start searching/traversing
            # from the top of the page; and we just need to continue from the position already in the parent.

            print("product_name_list:", product_name)

            if product_to_select.upper() in product_name.upper():
                # Add product into cart.
                productItem.find_element_by_css_selector("div button").click()  # or "div[2]/button"  or
                # "div/button" because the button object is unique only in all the 'div' below the parent.

                # Open the Shopping cart page by clicking the Checkout button:
                self.driver.find_element_by_css_selector("a[class*='btn-primary']").click()  # or
                # "//a[contains(@class,'btn-primary')]"

                # create a list with all the products in the shopping cart.
                # products_in_shopping_cart = driver.find_elements_by_css_selector("tbody tr")
                products_in_shopping_cart = self.driver.find_elements_by_xpath("//tbody/tr")

                # Loop to identify webElement/objects in the shopping cart.
                for productInShoppingCart in products_in_shopping_cart:
                    print("Whole product Object In Shopping Cart List: ", productInShoppingCart.text)

                    print("*****: ", productInShoppingCart.find_element_by_xpath("td[1]").text)
                    # in the shopping cart list, there are two lines that are not for product (total and a message)
                    # both of them have the value '&nbsp;' in the first 'td' child tag. this value indicate
                    # "non braking space" to the HTML; but in Selenium-Python code we treat it as single space "1".
                    # Therefore below 'if' avoid that the error:
                    # "selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate
                    # element: {"method":"xpath","selector":"td[1]/div[@class='media']/div/h4/a"}" in the next
                    # webDriver command to be executed (line 65 or 66), because these two rows do not have the element
                    # indicated there.
                    if productInShoppingCart.find_element_by_xpath("td[1]").text != " ":  # This is the value in the
                        # HTML code "&nbsp;", it is equal one space "1".

                        # identify the name of the product
                        # name_product_in_sc = productInShoppingCart.find_element_by_css_selector
                        #                                  ("td div[class='media'] div h4 a").text
                        name_product_in_sc = \
                            productInShoppingCart.find_element_by_xpath("td[1]/div[@class='media']/div/h4/a").text
                        print("name_product_in_sc:", name_product_in_sc)
                        if product_to_select.upper() in name_product_in_sc.upper():

                            assert name_product_in_sc == product_name

                            # Get the Quantity for the product in the Shopping Cart
                            # quantity_in_sc = productInShoppingCart.find_element_by_css_selector
                            #                                     ("td input").get_attribute("value")
                            quantity_in_sc = \
                                productInShoppingCart.find_element_by_xpath("td/input").get_attribute("value")
                            print("quantity_in_sc", quantity_in_sc)

                            # Get the Price for the product in the Shopping Cart
                            price_in_sc = productInShoppingCart.find_element_by_xpath("td[3]/strong").text
                            wk_list = price_in_sc.split(".")
                            price_in_sc = wk_list[1]
                            print("price_in_sc:", price_in_sc)

                            # Get the Total charge for the product in the Shopping Cart
                            total_in_sc = productInShoppingCart.find_element_by_xpath("td[4]/strong").text
                            wk_list = total_in_sc.split(".")
                            total_in_sc = wk_list[1]
                            print("total_in_sc", total_in_sc)

                            assert int(total_in_sc) == (int(quantity_in_sc) * int(price_in_sc))
                            product_found = True
                        else:
                            continue
                    else:
                        continue
                break
            else:
                continue

        if product_found:

            # click on the 'Checkout' button
            self.driver.find_element_by_css_selector("button[class*='btn-succe']").click()

            # type the delivery country location
            # elivery_country = "india"
            delivery_country = "United States of America"
            self.driver.find_element_by_id("country").send_keys(delivery_country)

            # to select the country:
            # Define explicit wait for the list of country to popup:
            six_seconds_wait_condition = WebDriverWait(self.driver, 6)  # Explicit wait applicable to certain
            # webDriver command
            six_seconds_wait_condition.until(expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div[class='suggestions'] ul li a")))

            # after list of country popped up, create countries_list
            countries_list = self.driver.find_elements_by_css_selector("div[class='suggestions'] ul li a")

            # loop the countries_list to click the desired country:
            for country in countries_list:
                if country.text.upper() == delivery_country.upper():
                    print("**** Delivery country:", country.text)
                    country.click()
                    break

            # six_seconds_wait_condition.until(expected_conditions.element_to_be_clickable(
            #    (By.CSS_SELECTOR, "div[class*='checkbox checkbox-primary']")))
            # the agree checkbox can not be clickable because the pop displayed in above search on country list block
            # it to be seen by Selenium WebDriver, therefore we have to execute a javaScript command to execute the
            # click of the checkbox, by using below set of instructions:
            # click on the 'I agree' checkbox
            agree_checkbox = self.driver.find_element_by_css_selector("div[class*='checkbox checkbox-primary']")
            if __name__ == '__main__':
                self.driver.execute_script("arguments[0].click();", agree_checkbox)
            # with above code we do not need the explicit wait of six seconds.

            # self.driver.find_element_by_xpath("//div[@class='checkbox checkbox-primary']/input[@id='checkbox2']").click()
            self.driver.find_element_by_css_selector("div[class*='checkbox checkbox-primary']").click()
            # self.driver.find_element_by_css_selector("input[id='checkbox2']").click()
            # notes: this radio button was not able to be located by using the id = checkbox2 with find_element_by_id or
            # even any one using the 'input' tag. Only successful when using the 'div' tag to identify the checkbox.
            # This error is generated:
            # selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element
            #         <input id="checkbox2" type="checkbox"> is not clickable at point (720, 243). Other element would
            #         receive the click: <label for="checkbox2">...</label>
            # the only locator working is find_element_by_css_selector("div[class*='checkbox checkbox-primary']") and
            # only with Chrome browser, with any other browser or locator type generates above error.

            # Click on the Purchase button:
            self.driver.find_element_by_css_selector("input[value='Purchase']").click()

            # to grab the value in the response message displayed, which is NOT a real alert that we can switch_to:
            alert_message = self.driver.find_element_by_class_name("alert-success")
            print("*** Alert Message:", alert_message.text)

            # now we can use Selenium to take a screenshot of the page with the successful message.
            self.driver.get_screenshot_as_file("finalScreenshot.png")  # this will be save in the project's root
            # directory.
            # note: we only take screenshot when one assertion fails, to help with the trouble shooting.

            print(" --- Product ", name_product_in_sc, "Found ---")
        else:
            print(" --- Product ", product_to_select, " NOT Found ---")
