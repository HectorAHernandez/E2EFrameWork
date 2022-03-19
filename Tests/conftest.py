import pytest
from selenium import webdriver

driver = None   # define the 'driver' object as a global variable and modify the fixture where the 'driver' object is
# created (the 'setup' fixture) with the command 'global driver' (which indicate, use the global variable defined for
# this class/conftest.py file. This needed for this global 'driver' object can be used in any other method defined in
# this conftest.py file, i.e. '_capture_screenshot(name' below.

gb_running_environment = None

# Defining the flag/hook to receive the 'browser_name' variable's value from the command prompt at execution time
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="my options: chrome OR firefox OR IE"
        # not the browser_name variable is available to the 'setup' fixture for setting the proper webDriver driver by
        # using the command: request.config.getoption("browser_name")
    )
    parser.addoption(
        "--product_to_buy", action="store", default="nokia", help="my options: Samsung, iphone, blackberry"
    )

    parser.addoption(
        "--running_environment", action="store", default="TEST", help="my options: test, production, staging"
    )

@pytest.fixture(scope="class")
def setup(request):   # Adding the 'request' object to be able to send the driver to the calling class using this
    #                   fixture. See 'request.cls.driver = driver' below.
    #     'request' is an object/parameter that will receive the parameter defined in the fixture (as a class level
    #     variable) and that need to be passed in each one of the iteration..

    global driver   # to indicate to use the global driver variable defined for this class/conftest.py file.
    global gb_running_environment  # to indicate to use the global variable gb_running_environment

    valid_browser = "YES"
    valid_running_environment = "YES"

    browser_name = request.config.getoption("browser_name")  # using request object to get the value of any
    # option/parameter/hook received at execution time. In this case the 'browser_name' option defined in
    # the pytest_addoption() method above.

    # below is still in practice:
    # wk_product_to_by = request.config.getoption("product_to_buy")
    # print("wk_product_to_by", wk_product_to_by)
    # request.cls.wk_product_to_buy = wk_product_to_by

    if browser_name.upper() == "CHROME":
        browser_options_object = webdriver.ChromeOptions()
        # browser_options_object.add_argument("--start-maximized")
        # browser_options_object.add_argument(("headless"))
        browser_options_object.add_argument("--ignore-certificate-errors")
        driver = webdriver.Chrome(executable_path="C:\\Selenium\\BrowserExecutableFiles\\chromedriver.exe",
                                  options=browser_options_object)
    elif browser_name.upper() == "FIREFOX":
        driver = webdriver.Firefox(executable_path="C:\\Selenium\\BrowserExecutableFiles\\geckodriver.exe")
    elif browser_name.upper() == "IE":
        driver = webdriver.Edge(executable_path="C:\\Selenium\\BrowserExecutableFiles\\msedgedriver.exe")
    elif browser_name.upper() == "OPERA":
        driver = webdriver.Opera(executable_path="C:\\Selenium\\BrowserExecutableFiles\\operadriver.exe")
    else:
        valid_browser = "NOT"
        driver = ""

    assert valid_browser == "YES", "Failing starting execution, this is an invalid browser name: "+browser_name

    gb_running_environment = request.config.getoption("running_environment")
    # using request object to get the value of any option/parameter/hook received at execution time. In this case
    # the 'running_environment' option defined in the pytest_addoption() method above.
    # gb_running_environment is a global variable to be used in the BaseClassUtilities.py to make it available to
    # all testCases needing to know the environment where the testCase is running.

    if gb_running_environment.upper() == "TEST":    # Open the applicatin in the test environment.
        driver.get("https://rahulshettyacademy.com/angularpractice/")
    elif gb_running_environment.upper() == "STAGING":
        driver.get("https://rahulshettyacademy.com/angularpractice/")
    elif gb_running_environment.upper() == "PRODUCTION":
        driver.get("https://rahulshettyacademy.com/angularpractice/")
    else:
        valid_running_environment = "NOT"

    assert valid_running_environment == "YES", "Failing starting execution, this is an invalid environment: "\
                                               + gb_running_environment

    print("Page title:", driver.title)
    driver.implicitly_wait(5)  # Implicit wait applicable to all webDriver commands.
    driver.maximize_window()

    request.cls.gb_running_environment = gb_running_environment  # assign the local value to the global variable.
    request.cls.driver = driver  # Assign the local driver 'driver' to the 'Request class' variable called 'driver' so
    # that it can
    #          be accessible to the class using this 'setup' fixture method. this is indicating the local driver
    #          object to be instantiated to a class-variable named 'driver' so that it can be inherited in the class
    #          using the 'setup' fixture by using the 'self.driver(...)' remember that 'self.' is used to access, by
    #          inheritance, any class level variable from a Parent class in a child class/method.
    #          request.cls.driver = driver --> define a class level object variable named 'driver' and assign the
    #          local object 'driver' created in this 'setup' method. By using this we avoid the error generated by the
    #          conflict created by the return command (I/O operation) with the yield command, because now we don't
    #          have any I/O operation, just saving the data of the local driver object into a class-variable.


    yield
    driver.close()


# Below is take screenshot when any testCase fail:
# NOTE: DO NOT rename or fix any typo in below code. it is taken as it is.
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)



