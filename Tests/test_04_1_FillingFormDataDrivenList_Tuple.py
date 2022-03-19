# This program fill out a form in a page by provisioning the data using parameterization from a
# @pytest.fixture defined in this testCase/program (look at the bottom).
# The @pytest.fixture define a Python List data structure with "tuple" data structure as its elements,so
# that the testCase repeats execution n times the number of tuple elements in the List structure.
# The elements in the tuple data structure are passed to the send_keys("input_data") using the index of the
# element in the tuple [0], [1], [3]...
# Note: this @fixture is defined here instead of in the conftest.py file, because this @Fixture define
# data only applicable or common to this testCase/program.
import pytest

from PageObjects.HomePage import HomePage
from utilities.BaseClassUtilities import BaseClassUtilities


class TestFormDataDriven(BaseClassUtilities):
    def test_home_page_form_provision(self, get_home_page_data):  # now this test call the fixture 'get_home_page_data'
        # defined in this program at the bottom.

        home_page = HomePage(self.driver)

        home_page.get_user_name().send_keys(get_home_page_data[0])  # now using element at index '0' in the tuple
        # received/inherited as a parameter from the 'get_home_page_data' fixture.
        # this was replaced by above command: home_page.get_user_name().send_keys("Hector")
        home_page.get_email().send_keys(get_home_page_data[1])
        home_page.get_love_ice_cream_check().click()

        # Use a utility function to select by text from an Static Dropdown List:
        select_static_drop_down_list_by_text(home_page.get_gender_listbox(), get_home_page_data[2])

        # The Python Selenium webDriver commands for the "Submit" button could be:
        home_page.get_submit_button().click()

        alert_text = home_page.get_result_message().text
        assert "Success" in alert_text, "Process not successful"

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

    @pytest.fixture(params=[("hector", "ghector@gmail.com", "Male"), ("Gene", "decode@de.com", "Female"),
                            ("Gisela", "Amparo@put.com", "Female")])
    def get_home_page_data(self, request):
        return request.param
        # this will send/return each tuple to the testCase calling this @pytest.fixture one
        # tuple at at time.
