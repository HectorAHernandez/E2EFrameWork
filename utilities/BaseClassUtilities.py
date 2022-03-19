import inspect

import pytest
import logging
from selenium.webdriver.support.select import Select


def select_static_drop_down_list_by_text(parm_locator, search_text):

    # Static Dropdown List handling:
    # Selenium WebDriver has a special class called "Select" (with uppercase 'S') which provides all the methods to
    # handle the options in the dropdown list fields/object. This Select class can only be used if the
    # tag name of the html webpage object is "select".
    # To use these methods we have to create/instantiate an object of this Select class as follow:
    static_listbox = Select(parm_locator)

    # used as the locator of the gender dropdown object in the webpage.
    # the first time using the select() class we will be prompted to import it from
    # (selenium.webdriver.support.select import Select)
    # now using the methods in the created object we can select the option we want using the method we want:
    static_listbox.select_by_visible_text(search_text)
    # static_listbox.select_by_index(0)  # the index of the options, starting in 0, 1, 2 ... n-1 0=Male.


def get_logger():
    logger_name = inspect.stack()[1][3]    # contains the name of the program calling this get_logger() method

    hector_logger = logging.getLogger(logger_name)
    # previous: hector_logger = logging.getLogger(__name__)
    file_handler_log_file = logging.FileHandler("hectorLogFile_InClass02.log")  # connect file location to fileHandle
    # OR to place the file in a directory:
    # file_handler_log_file = logging.FileHandler("C:\Users\ssshh\PycharmProjects\HectorFirstpythonProject\usingPyTestDemo\LogReports\hectorLogFile_02.log")
    first_formatter_object = logging.Formatter("%(asctime)s  :  %(name)s  :  %(levelname)s  :  %(message)s ")
    file_handler_log_file.setFormatter(first_formatter_object)  # connect formatter to fileHandle.
    hector_logger.handlers.clear()  # this avoid the repetition of n times the same log info in the log.
    hector_logger.addHandler(file_handler_log_file)  # Connect the fileHandler to the logger and we are almost ready.
    hector_logger.setLevel(logging.INFO)

    return hector_logger


@pytest.mark.usefixtures("setup")  # Connect to the 'setup' fixture so that all utilities codes and driver's
# definitions and setting can be inherited by all the other classes containing all the testCases, when they use
# the 'BaseClassUtilities' class.
class BaseClassUtilities:
    # pass   # pass is a place holder statement. Do nothing
    # pass

    def get_gv_running_environment(self):
        return self.gb_running_environment


def main():
    pass

if __name__ == "__main__":
    main()

