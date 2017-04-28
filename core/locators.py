from selenium.webdriver.common.by import By


class HomePageLocators(object):
    SEARCH_BUTTON = (By.CSS_SELECTOR, '#search-form-property button')
    SEARCH_INPUT = (By.CSS_SELECTOR, '#search-form-property .tt-input')


class SearchResultsLocators(object):
    SEARCH_RESULT_CONTAINER = (By.ID, 'primary-content')