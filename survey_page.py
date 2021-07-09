from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from finish_page import finish_page


def find(func, *args):
    try:
        return func(*args)
    except NoSuchElementException:
        return None


def find_by_xpath_from_element(elem, *args):
    try:
        return elem.find_element_by_xpath(*args)
    except NoSuchElementException:
        return None


class survey_page:
    def __init__(self, driver, season):
        self.season = season
        self.driver = driver
        self.site_path = "http://" + season + ".survey.moevm.info/"
        self.current_name_teacher = None
        self.current_subject = None
        self.current_num_in_menu = 1

    def is_compulsory_rating_current_subject(self, rating):
        if self.current_name_teacher is None:
            return None
        else:
            if rating == "relevance":
                num_span = 1
            elif rating == "quality":
                num_span = 2
            else:
                return None
            xpath = f'//a[@name="{self.current_name_teacher}"]/following::div[1][@class="content"]/b[2][text()' \
                    f'="{self.current_subject}"]/following-sibling::span[{num_span}][contains(text(), "*")]'
            find_func = self.driver.find_element_by_xpath
            compulsory = find(find_func, xpath)
            if compulsory is None:
                return None
            else:
                return True

    def get_teacher_names(self):
        xpath = '//a[@name]'
        find_func = self.driver.find_elements_by_xpath
        teachers = find(find_func, xpath)
        names = []
        for t in teachers:
            names.append(t.get_attribute("name"))
        if names is None:
            return None
        else:
            return names

    def go_to_next_teacher(self):
        if self.current_name_teacher is None:
            xpath = '//a[@name]'
        else:
            xpath = f'//a[@name="{self.current_name_teacher}"]/following::div[1][@class="content"]/b[2][text()' \
                    f'="{self.current_subject}"]/following-sibling::a[@name] '
        find_func = self.driver.find_element_by_xpath
        next_teacher = find(find_func, xpath)
        if next_teacher is None:
            return None
        else:
            self.current_name_teacher = next_teacher.get_attribute("name")
            xpath = './following::div[1][@class="content"]/b[2]'
            next_subject = find_by_xpath_from_element(next_teacher, xpath)
            if next_subject is None:
                return None
            else:
                self.current_subject = next_subject.text

        return self.current_name_teacher

    def go_to_next_teacher_in_menu(self):
        xpath = f'//div[@id="menu"]/div[@class="menu-container"][{self.current_num_in_menu}]/a/h5'
        self.current_num_in_menu += 1
        find_func = self.driver.find_element_by_xpath
        next_teacher_in_menu = find(find_func, xpath)
        if next_teacher_in_menu is None:
            return None
        else:
            current_name_teacher_in_menu = next_teacher_in_menu.text

        return current_name_teacher_in_menu

    def choose_rating_relevance(self, rating):
        if self.current_name_teacher is None:
            return None
        else:
            xpath = f"//a[@name='{self.current_name_teacher}']/following::div[1][@class='content']/b[2][text(" \
                    f")='{self.current_subject}']/following::div[@data-toggle][1]//input[@value='{rating - 1}'] "
        find_func = self.driver.find_element_by_xpath
        radio_rating = find(find_func, xpath)
        if radio_rating is None:
            return None
        else:
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath))))

            return radio_rating

    def choose_rating_quality(self, rating):
        if self.current_name_teacher is None:
            return None
        else:
            xpath = f"//a[@name='{self.current_name_teacher}']/following::div[1][@class='content']/b[2][text(" \
                    f")='{self.current_subject}']/following::div[@data-toggle][2]//input[@value='{rating - 1}'] "
        find_func = self.driver.find_element_by_xpath
        radio_rating = find(find_func, xpath)
        if radio_rating is None:
            return None
        else:
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath))))
            return radio_rating

    def click_finish_button(self):
        xpath = f'//div[@id="div_submit_results"]//button[@id="submit_results"]'
        find_func = self.driver.find_element_by_xpath
        button_finish = find(find_func, xpath)
        if button_finish is None:
            return None
        else:
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath))))
            return True

    def click_finish_button_success(self):
        if self.click_finish_button() is True:
            return finish_page(self.driver, self.season)
        else:
            return None

    def click_finish_button_alert(self):
        if self.click_finish_button() is True:
            return survey_page(self.driver, self.season)
        else:
            return None

    def find_alert(self):
        xpath = '//div[@id="div_submit_results"]//div[@role="alert"]//strong'
        find_func = self.driver.find_element_by_xpath
        alert = find(find_func, xpath)
        if alert is None:
            return None
        else:
            return alert