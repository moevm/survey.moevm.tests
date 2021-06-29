from selenium.common.exceptions import NoSuchElementException
from survey_page import survey_page
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def find(func, *args):
    try:
        return func(*args)
    except NoSuchElementException:
        return None


def values_child_elements(elem, css_selector):
    elements = elem.find_elements_by_css_selector(css_selector)
    values = []
    for el in elements:
        value = el.get_attribute("value")
        if value is not None:
            values.append(value)
    return values


def count_child_elements(elem, css_selector):
    try:
        return len(elem.find_elements_by_css_selector(css_selector))
    except NoSuchElementException:
        return None


class start_page:
    def __init__(self, driver, season):
        self.season = season
        self.driver = driver
        self.site_path = "http://{}.survey.moevm.info/".format(season)
        self.nums_directions = [1, 2, 3, 4]

    def count_directions(self):
        xpath = "//div[@class='radio btn_choice_sem']"
        find_func = self.driver.find_element_by_xpath
        radio_btn_choice = find(find_func, xpath)
        if radio_btn_choice is None:
            return 0
        else:
            css_selector = "label"
            return count_child_elements(radio_btn_choice, css_selector)

    def semesters_from_direction(self, direction):
        self.choose_direction(direction)
        xpath = '//div[@id="div_sem_choice"]'
        find_func = self.driver.find_element_by_xpath
        radio_btn_choice = find(find_func, xpath)
        if radio_btn_choice is None:
            return 0
        else:
            css_selector = "div.radio label input"
            return values_child_elements(radio_btn_choice, css_selector)

    def choose_direction(self, num_direction):
        xpath = '//div[@class="radio btn_choice_sem"]//input[@value="{}"]'.format(num_direction)
        find_func = self.driver.find_element_by_xpath
        radio_direction = find(find_func, xpath)
        if radio_direction is None:
            return None
        else:
            radio_direction.click()
            return num_direction

    def choose_sem(self, num_sem):
        xpath = '//div[@id="div_sem_choice"]//input[@value="{}"]'.format(num_sem)
        find_func = self.driver.find_element_by_xpath
        radio_sem = find(find_func, xpath)
        if radio_sem is None:
            return None
        else:
            radio_sem.click()
            return num_sem

    def write_id(self, input_id):
        id = "ID"
        find_func = self.driver.find_element_by_id
        field_id = find(find_func, id)
        if field_id is None:
            return None
        else:
            field_id.send_keys(input_id)
            value_id = field_id.get_attribute("value")
            return value_id

    def click_start_button(self):
        xpath = '//div[@id="btn-submit"]//button[@class="btn btn-outline-dark"]'
        find_func = self.driver.find_element_by_xpath
        button_start = find(find_func, xpath)
        if button_start is None:
            return None
        else:
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath))))
            return True

    def click_start_button_success(self):
        if self.click_start_button() is True:
            return survey_page(self.driver, self.season)
        else:
            return None

    def click_start_button_alert(self):
        if self.click_start_button() is True:
            return start_page(self.driver, self.season)
        else:
            return None

    def find_alert(self):
        xpath = '//div[@id="alert"]//div[@role="alert"]//strong'
        find_func = self.driver.find_element_by_xpath
        alert = find(find_func, xpath)
        if alert is None:
            return None
        else:
            return alert
