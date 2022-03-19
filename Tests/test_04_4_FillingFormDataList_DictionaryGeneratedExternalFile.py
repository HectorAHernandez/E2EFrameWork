# This program fill out a form in a page by provisioning the data using parameterization from a
# @pytest.fixture defined in this testCase/program (look at the bottom).
# The @pytest.fixture define a Python List data structure with "Dictionary" data structure as its elements,so
# that the testCase repeats execution n times the number of "Dictionary" elements in the List structure.
# The Dictionary Python data structure is defined as {"key_name_1":"value_1", "key_name_2":"value_2"....} using
# '{' and '}' instead of '(' and ')' like in the tuple. The List Python data structure uses '[' and ']'.
# The elements in the Dictionary data structure are passed to the send_keys("input_data") using the key_name and
# the corresponding pair 'value' of the key_name is returned.
# THE DICTIONARY IS DEFINED IN AN EXTERNAL FILE (IN A NEW TestData Python package) and in this external file a
# class is defined to contain variable/object with the Lists data structure for all the data needed to be used
# for all the testCases.
# THEN IN THE @pytest.fixture we have to modify the params= command to use this new variable defined in this new
# test class. '@pytest.fixture(params=AllTestsTestData.home_page_test_data_1)' (see below) instead of the
# List with all the test data to be used for the testCase.

# Note: this @fixture is defined here instead of in the conftest.py file, because this @Fixture define
# data only applicable or common to this testCase/program.

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

# # this is the program that create the below TestLoginData.selected_users: testhh_05_2_Excel_To_Dictionary_File.py

import logging

import pytest
from PageObjects.HomePage import HomePage
from TestData.AllPagesTestData import AllTestsTestData
from TestData.usersLogin import TestLoginData
from utilities.BaseClassUtilities import BaseClassUtilities, select_static_drop_down_list_by_text, get_logger


class TestFormDataDriven(BaseClassUtilities):
    running_environment = "test"
    test_01 = "AllTestsTestData.home_page_test_data_env_"+running_environment
    print("test_01: ", test_01)

    def test_home_page_form_provision(self, get_home_page_data_with_dict_external):  # now this test call the
        # fixture 'get_home_page_data' defined in this program at the bottom.

        log = get_logger()  # instantiate a log object to use the logging methods.
        log.info("*** Starting Execution  ***")
        log.setLevel(logging.INFO)   # set the logging level in this testCase overwriting the one in the
        # BaseClassUtilities.py class get_logger() method.

        global running_environment
        running_environment = self.get_gv_running_environment()

        home_page = HomePage(self.driver)

        print("get_home_page_data_with_dict_external: ", get_home_page_data_with_dict_external)

        home_page.get_user_name().send_keys(get_home_page_data_with_dict_external["name"])  # now using element at
        # index '0' in the tuple received/inherited as a parameter from the 'get_home_page_data' fixture.
        # this was replaced by above command: home_page.get_user_name().send_keys("Hector")
        print("only name keyword: ", get_home_page_data_with_dict_external["name"])

        home_page.get_email().send_keys(get_home_page_data_with_dict_external["email"])
        home_page.get_love_ice_cream_check().click()

        # Use a utility function to select by text from an Static Dropdown List:
        select_static_drop_down_list_by_text(home_page.get_gender_listbox(),
                                             get_home_page_data_with_dict_external["gender"])

        # The Python Selenium webDriver commands for the "Submit" button could be:
        home_page.get_submit_button().click()
        log.info("*** Submitted data for user: " + get_home_page_data_with_dict_external["name"])

        alert_text = home_page.get_result_message().text
        assert "Success" in alert_text, "Process not successful"
        log.info("*** Data Processed Successfully")

        self.driver.refresh()
    # This refresh is needed to erase all previous data provisioned to the page so
    # that the next iteration of the testCase execution find all field empty and avoid appending the data
    # on top of the previous iteration one. The page data is refreshed everytime that the driver.get(url)
    # command is executed or when the page is launched by first time, but in this case it was executed only
    # once in the 'setup' @pytest.fixture in the conftest.py.

    # Create the @pytest.fixture to implement parameterization while provisioning the data to this page.
    # - The fixture define the use of parameters using a List Python data structure which elements are tuple
    #   data structure.
    # - The test will be repeated as number of tuples are defined in the List:

    # selecting data from the specific variable with the test data we want to use for the test.
    # this is the program that create the below TestLoginData.selected_users: testhh_05_2_Excel_To_Dictionary_File.py
    @pytest.fixture(params=TestLoginData.selected_users)
    def get_home_page_data_with_dict_external(self, request):
        return request.param
        # this will send/return each tuple to the testCase calling this @pytest.fixture one
        # tuple at at time.
