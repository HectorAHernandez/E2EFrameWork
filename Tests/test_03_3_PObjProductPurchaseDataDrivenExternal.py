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

#       Start of program test_02PageObjectSelectProductPurchase.py
# FW-6  For moving all the page webelements object defined in this code to their corresponding page object class, let's
#       create a the "PageObjects" python package, in it, one python.py file for each page referenced as a class and
#       move all page's objects definition code from this program to each one defined page classes.
#       Now to access all the webElements defined in the page classes we have to use the getter and setter methods
#       defined in the page class, And to make the getter and setter methods available we have to instantiate and
#       object of the page class i.e. homePageObject = HomePage(driver), passing the 'driver' as a parameter because
#       all the getter and setter method expect the 'driver' object as a parameter.

# FW-7  Replace ALL direct webElement reference by the use of the getter and setter in the instantiated page object:
#         home_page_object.get_shop_link().click()
#         this is the before way: 'self.driver.find_element_by_css_selector("a[href*='shop']").click()'

# FW-8  Insert the INTER-LINK concept for the automatic navigation between pages, this is implemented by replacing
#       the all page's object instantiation from the testCase code and moving it to the Page class based on the
#       synchronization of after the click/integration point that triggers the new page. To implement this we have
#       to move the clicking of the button/link method from the testCase TO the code in then button/link method and
#       after it add the instantiation of the next page to be triggered
#       Now, in the HomePage class, the get_shop_link() method click on the link, instantiate the object for the new
#       displayed page and return the driver's object of this new page to the testCase. so we have to remove the
#       click() from testCase.
#       def get_shop_link(self):
#           self.driver.find_element(*HomePage.shop_link).click()
#           checkout_page_object = CheckoutPage(self.driver)
#           return checkout_page_object

# FW-9  Inserting dataDriven using @pytest.fixture for receiving the product to buy from an external test file,
#       this was accomplished by with below fixture at the bottom of this class:
#           @pytest.fixture(params=AllTestsTestData.buy_product_test_data_1)
#           def get_product_to_buy_data(self, request):
#           return request.param
#       Then then inserting the fixtured method get_product_to_by_data into the testCase declaration to indicate that
#       the testCase will be receiving data from this fixture (which is for using a Dictionary Python data structure
#       in a Test Data variable defined in an external Data file in TestData Python package).
#       Then to use the values defined in the Dictionary we use the fixtured method name (get_product_to_buy_data) and
#       the key-name of the ("key": "value") pair in the Dictionary: get_product_to_buy_data["product"]

# FW-10 Implementing Logging fixture to create the log of what we want to log from the testCase execution:
#       Copy/Create the "def get_logger():" method, as static method, in the "BaseClassUtilities.py" to have this
#       method available, as an utility to all the testCases. It was as static because it does not modify any data and
#       we want code to be available as global.
#       Now in each one of the test cases, at the beginning, instantiate an object of this logger method, so that we
#       can use it to call the method defined in the logger method from the BaseClassUtilities.py class.

# FW-11 Creating .html report with the result of each testCase and the information logged in the logging file:
#       we have to install the html plugin/utility in the PyCharm IDE with this command: pip install pytest-html.
#       then adding this flag to the test case execution command: py.test testCase.py --html=myReportName.html.
#           C:\Users\ssshh\PycharmProjects\E2EFrameWork\Tests>
#                 py.test test_03_3_PObjProductPurchaseDataDrivenExternal.py --html=ResultsReport.html
#       Then opening the html report created in a browser tab to see the logged messages in Report detail:
#           file://C:\Users\ssshh\PycharmProjects\E2EFrameWork\Tests\ResultsReport.html
#       NOTE: For the logged information to be included in the html file, the execution command must not
#             include the flags: -v -s. This is only:
#                   py.test test_03_3_PObjProductPurchaseDataDrivenExternal.py --html=ResultsReport.html

# FW-12 To take screenshot when any step fail we have to:
#       1- In conftest.py define de variable for the 'driver' object as global and initialize it with value 'None':
#               driver = "None"
#       2- Modify the 'setup' fixture to indicate to use the global 'driver' variable, by inserting below command
#          as the very first line: 'global driver'
#       3- Create a the new fixture 'pytest_runtest_makreport(item) using below code, without changing anything, in the
#          conftest.py file:
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """
#         Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
#         :param item:
#         """
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_") + ".png"
#             _capture_screenshot(file_name)
#             if file_name:
#                 html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % file_name
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra
#
#       4- Below the added fixture, add below method to take the screenshot
# def _capture_screenshot(name):
#         driver.get_screenshot_as_file(name)

import logging

import pytest
from PageObjects.HomePage import HomePage
from TestData.AllPagesTestData import AllTestsTestData
from utilities.BaseClassUtilities import BaseClassUtilities, get_logger


# @pytest.mark.usefixtures("setup")    commented to be eliminated, because now we are using the BaseClassUtilities,
# which contains the 'setup' fixture invocation and any other general use utility code. Because now, by inheritance,
# this TestEndtoEndShop class, has access or knowledge of the 'setup' fixture and don't need to invoke it by itself


class TestEndToEndShop(BaseClassUtilities):

    def test_select_product_and_purchase(self, get_product_to_buy_data):   # setup was eleminated because with 'self' we
        # have now access to all the code in the parent class BaseClassUtilities, including the 'setup' fixture.
        # def test_select_product_and_purchase(self, setup):

        # instantiate a log object from the logger method in the BaseClassUtilities.py class. The 'self.' is not needed
        # in '= get_logger()' because the get_logger() method was defined as static in the BaseClassUtilities.py and
        # imported in this testCase with 'from utilities.BaseClassUtilities import BaseClassUtilities, get_logger':
        log = get_logger()  # Now we can use this 'log' object to log what we want see below:
        log.info("**** Started execution for test case: ")

        log.setLevel(logging.DEBUG)  # to change the log level in the testCase instead of the log definition.
        log.info("GLOBAL ENVIRONMENT: " + self.get_gv_running_environment())

        # initialize wk_product_to_select:
        wk_product_to_select = get_product_to_buy_data["product"]
        log.debug("-- wk_product_to_select " + wk_product_to_select)

        wk_product_found = False
        wk_name_product_in_sc = ""

        # instantiate a pageObject of the HomePage class, passing this instance driver 'self.driver' object as a
        # parameter to the HomePage class's constructor method:
        home_page_object = HomePage(self.driver)

        # click on the Shop link, we will use the inter-link concept implemented on the page's classes. where
        # we will use the method in the current page that click the link and at the same time instantiate and
        # return the driver object for the next page (checkout_page_object) (this is inter-link):
        checkout_page_object = home_page_object.get_shop_link()  # this get_shop_link() method will click on the
        # link button then instantiate the object of the displayed page and return it to this testCase to continue
        # the execution using all the getter and setter methods for the displayed page.

        # No need to instantiate a checkoutPage object from the CheckoutPage class, because of what explained above.
        # ##   --> checkout_page_object = CheckoutPage(self.driver)

        # 1: Build a list of all the products displayed:
        i = -1  # create index variable to access the tuple data structure returned into products_list for
        #         the checkout_page_object
        products_name_list = checkout_page_object.get_product_names_list()
        for product_name in products_name_list:
            i = i + 1
            wk_product_name_in_prod_list = product_name.text

            log.debug("current product_name_list in products list: " + wk_product_name_in_prod_list)
            if wk_product_to_select.upper() in wk_product_name_in_prod_list.upper():
                # Add product into cart.
                checkout_page_object.get_add_to_cart_buttons_list()[i].click()
                #  old: productItem.find_element_by_css_selector("div button").click()
                log.info("**** Added this product to the cart: " + wk_product_name_in_prod_list)

                # Open the Shopping cart page by clicking the Checkout button:
                checkout_page_object.get_checkout_button().click()
                log.info("**** Clicked checkout button to go to the Shopping Cart")

                # create a list with all the products in the shopping cart.
                products_in_shopping_cart = checkout_page_object.get_products_in_shopping_cart_list()
                # above replaced: products_in_shopping_cart = self.driver.find_elements_by_xpath("//tbody/tr")

                # Loop to identify webElement/objects in the shopping cart.
                for productInShoppingCart in products_in_shopping_cart:
                    log.debug("-- Whole product Object In Shopping Cart List: " + productInShoppingCart.text)

                    log.debug("-- Shopping Cart Product: " + productInShoppingCart.find_element_by_xpath("td[1]").text)
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
                        # identify the name of the product in the shopping cart
                        wk_name_product_in_sc = checkout_page_object.get_product_in_shopping_cart_name().text
                        log.debug("-- wk_name_product_in_sc: " + wk_name_product_in_sc)

                        if wk_product_to_select.upper() in wk_name_product_in_sc.upper():
                            assert wk_name_product_in_sc == wk_product_name_in_prod_list

                            # Get the Quantity for the product in the Shopping Cart
                            wk_quantity_in_sc = checkout_page_object.get_product_in_shopping_cart_quantity().\
                                get_attribute("value")
                            log.debug("-- wk_quantity_in_sc " + wk_quantity_in_sc)

                            # Get the Price for the product in the Shopping Cart
                            wk_price_in_sc = checkout_page_object.get_product_in_shopping_cart_price().text
                            wk_list = wk_price_in_sc.split(".")
                            wk_price_in_sc = wk_list[1]
                            log.debug("-- wk_price_in_sc: " + wk_price_in_sc)

                            # Get the Total charge for the product in the Shopping Cart
                            wk_total_in_sc = checkout_page_object.get_product_in_shopping_cart_total().text
                            wk_list = wk_total_in_sc.split(".")
                            wk_total_in_sc = wk_list[1]
                            log.debug("-- wk_total_in_sc" + wk_total_in_sc)

                            log.info("**** Added product product " + wk_name_product_in_sc + ", is in Shopping Cart "
                                     + "With total charge of:" + wk_total_in_sc)

                            assert int(wk_total_in_sc) == (int(wk_quantity_in_sc) * int(wk_price_in_sc))
                            #  assert int(wk_total_in_sc) == 2500  # to force the failing.
                            wk_product_found = True
                            break
                        else:
                            continue
                    else:
                        continue
                break
            else:
                continue

        if wk_product_found:

            # type the delivery country location
            # elivery_country = "india"
            wk_delivery_country = get_product_to_buy_data["deliveryCountry"]

            # click on the 'Final Checkout' button and instantiate object for the next page displayed, (in this
            # case the purchase_page, this is inter-linking pages):
            purchase_page_object = checkout_page_object.get_final_checkout_button_click()
            # no need instantiate an object of the PurchasePage class in this testCase code
            #  ---> purchase_page_object = PurchasePage(self.driver)

            # typing the country name to delivery the purchase order
            purchase_page_object.get_country_name().send_keys(wk_delivery_country)

            # to select the country from the dynamic country dropdown listbox:
            # after list of country popped up, create countries_list
            countries_list = purchase_page_object.get_countries_list()

            # loop the countries_list to click the desired country:
            for country in countries_list:
                if country.text.upper() == wk_delivery_country.upper():
                    print("**** Delivery country:", country.text)
                    country.click()
                    break

            # the agree checkbox can not be clickable because the pop displayed in above search on country list block
            # it to be seen by Selenium WebDriver, therefore we have to execute a javaScript command to execute the
            # click of the checkbox, by using below set of instructions:
            # click on the 'I agree' checkbox
            agree_checkbox = purchase_page_object.get_agree_checkbox()
#            if __name__ == '__main__':  I don't know where this if __name--- code came from.
            self.driver.execute_script("arguments[0].click();", agree_checkbox)

            # This driver.execute_script() JavaScript code avoid the generation of this error:
            # selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element
            #         <input id="checkbox2" type="checkbox"> is not clickable at point (720, 243). Other element would
            #         receive the click: <label for="checkbox2">...</label>

            # Click on the Purchase button:
            purchase_page_object.get_purchase_button().click()

            # to grab the value in the response message displayed, which is NOT a real alert that we can switch_to:
            wk_response_message = purchase_page_object.get_response_message().text
            log.debug("-- Response Message: " + wk_response_message)

            # now we can use Selenium to take a screenshot of the page with the successful message.
            self.driver.get_screenshot_as_file("finalScreenshot.png")  # this will be save in the project's root
            # directory.
            # note: we only take screenshot when one assertion fails, to help with the trouble shooting.

            print(" --- Product ", wk_name_product_in_sc, "Found ---")
            log.info("**** Product successfully ordered and sent to country: " + wk_delivery_country)
        else:
            print(" --- Product ", wk_product_to_select, " NOT Found ---")
            log.info("**** This Product was NOT FOUND: " + wk_product_to_select)

        self.driver.back()

    @pytest.fixture(params=AllTestsTestData.buy_product_test_data_1)
    def get_product_to_buy_data(self, request):
        return request.param
