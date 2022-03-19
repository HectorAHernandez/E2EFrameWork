# This program fill out a form in a page by provisioning the data directly in the program as fixed values
# in the send_keys("input_data")

from PageObjects.HomePage import HomePage
from utilities.BaseClassUtilities import BaseClassUtilities


class TestFormDataDriven(BaseClassUtilities):

    def test_form_provision(self):

        home_page = HomePage(self.driver)

        home_page.get_user_name().send_keys("Hector")
        home_page.get_email().send_keys("hhernandez@gmail.com")
        home_page.get_love_ice_cream_check().click()

        # Use a utility function to select by text from an Static Dropdown List:
        select_static_drop_down_list_by_text(home_page.get_gender_listbox(), "Female")

        # The Python Selenium webDriver commands for the "Submit" button could be:
        home_page.get_submit_button().click()

        alert_text = home_page.get_result_message().text
        assert "Success" in alert_text, "Process not successful"

        self.driver.refresh()   # This refresh is needed to erase all previous data provisioned to the page so
        # that the next iteration of the testCase execution find all field empty and avoid appending the data
        # on top of the previous iteration one. The page data is refreshed everytime that the driver.get(url)
        # command is executed or when the page is launched by first time, but in this case it was executed only
        # once in the 'setup' @pytest.fixture in the conftest.py.

# with this method/solution, if we want to provision data for another user then we have to repeat the same set
# of instructions but with the new user data, this no an efficient way but it is used as learning to make it
        # better in the next program:
        home_page.get_user_name().send_keys("Raphael")
        home_page.get_email().send_keys("Rapha888@gmail.com")
        home_page.get_love_ice_cream_check().click()

        # Use a utility function to select by text from an Static Dropdown List:
        select_static_drop_down_list_by_text(home_page.get_gender_listbox(), "Male")

        # The Python Selenium webDriver commands for the "Submit" button could be:
        home_page.get_submit_button().click()

        alert_text = home_page.get_result_message().text
        assert "Success" in alert_text, "Process not successful"