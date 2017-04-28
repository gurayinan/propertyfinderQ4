from modules import *


class PropertyFinder(object):

    def __init__(self):
        try:
            self.settings_location = os.path.join(os.getcwd(), 'core', 'settings.ini')
            self.excel_location = os.path.join(os.getcwd(), 'core', 'data.xlsx')
            self.settings = {}
            self.parse_settings()
            self.read_excel()
            self.driver = None
            self.init_driver()
            self.ec = ec
            self.wait = WebDriverWait(self.driver, 20)
            self.action = ActionChains(self.driver)
        except StandardError:
            raise

    """
    Reads settings.ini file to set required array
    """
    def parse_settings(self):
        config = ConfigParser.ConfigParser()
        config.read(self.settings_location)
        for section in config.sections():
            for option in config.options(section):
                self.settings[option] = config.get(section, option)

    """
    Reads parameters from excel file for Data Driven Testing
    """
    def read_excel(self):
        excel = openpyxl.load_workbook(self.excel_location)
        sheet = excel.get_sheet_by_name('Sheet 1')
        self.settings['search_string'] = sheet['A3'].value
        self.settings['min_bedrooms'] = sheet['B3'].value
        self.settings['order_by'] = sheet['C3'].value

    """
    Initialize Chrome Driver
    """
    def chrome(self):
        self.driver = webdriver.Chrome(executable_path=self.settings.get('driver_path'))
        width = self.driver.execute_script("return window.screen.availWidth")
        height = self.driver.execute_script("return window.screen.availHeight")
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(width, height)

    """
    Initialize Firefox Driver
    """
    def firefox(self):
        self.driver = webdriver.Firefox(executable_path=self.settings.get('driver_path'))
        self.driver.maximize_window()

    """
    Select browser upon settings.ini
    """
    def init_driver(self):
        desired_browser = str(self.settings.get('selected_browser'))
        current_os = sys.platform
        browser_location = "core/drivers/{browser}driver{os}"
        if current_os == "linux2":
            self.settings["driver_path"] = browser_location.format(os="Linux64", browser=desired_browser)
        elif current_os == "darwin":
            self.settings["driver_path"] = browser_location.format(os="Mac64", browser=desired_browser)
        elif current_os == "win32":
            self.settings["driver_path"] = browser_location.format(os="Win64.exe", browser=desired_browser)
        browser = getattr(self, desired_browser)
        browser()


class MainPageObject(PropertyFinder):

    def search_properties(self):
        search_for = self.settings.get('search_string')
        min_bed_count = self.settings.get('min_bedrooms')
        self.wait.until(ec.element_to_be_clickable(HomePageLocators.SEARCH_INPUT)).send_keys(search_for)
        time.sleep(2)
        self.driver.execute_script('$(".tt-suggestion:first").click()')
        self.driver.execute_script("$('select[name=\"bf\"]').attr('style','display:block')")
        select = Select(self.driver.find_element_by_name('bf'))
        select.select_by_visible_text(min_bed_count)
        self.driver.execute_script("$('select[name=\"bf\"]').attr('style','display:none')")
        self.wait.until(ec.element_to_be_clickable(HomePageLocators.SEARCH_BUTTON)).click()


class SearchResultsPageObject(PropertyFinder):

    def sort_properties(self):
        sort_by = self.settings.get('order_by')
        self.driver.execute_script("$('select[name=\"search-order-by\"]').attr('style', 'display:block')")
        sort_by_selector = Select(self.driver.find_element_by_name('search-order-by'))
        sort_by_selector.select_by_visible_text(sort_by)
        self.driver.execute_script("$('select[name=\"search-order-by\"]').attr('style', 'display:none')")
        self.wait.until(ec.visibility_of_element_located(SearchResultsLocators.SEARCH_RESULT_CONTAINER))

    def select_last_property(self):
        search_results = self.driver.find_elements_by_class_name('listing-content')
        search_results[-1].click()
        bed_count = self.driver.execute_script("return $('.fixed-table tr > th:contains(\"Bedrooms\")').next().html()")
        return bed_count



