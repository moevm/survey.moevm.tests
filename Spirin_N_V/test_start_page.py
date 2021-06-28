from start_page import start_page
import unittest
from selenium.webdriver import Chrome


class test_start_page(unittest.TestCase):
    season = "autumn"
    page = start_page(Chrome(), season)
    driver = page.driver
    driver.get(page.site_path)

    def tearDown(self):
        self.page = start_page(self.driver, self.season)
        self.driver.get(self.page.site_path)

    def test_choosing_directions(self):
        for direction in self.page.nums_directions:
            choosing_direction = self.page.choose_direction(direction)
            self.assertNotEqual(choosing_direction, None, "Не удалось найти " + direction.__str__() + " направление!")

    def test_choosing_semesters_from_first_direction(self):
        self.page.choose_direction(1)
        nums_semesters = [1, 3, 5, 7]
        for num_sem in nums_semesters:
            choosing_sem = self.page.choose_sem(num_sem)
            self.assertNotEqual(choosing_sem, None, "Не удалось найти " + num_sem.__str__() + " семестр после выбора "
                                                                                              "первого направления!")

    def test_choosing_semesters_from_second_direction(self):
        self.page.choose_direction(2)
        nums_semesters = [1, 3, 5, 7]
        for num_sem in nums_semesters:
            choosing_sem = self.page.choose_sem(num_sem)
            self.assertNotEqual(choosing_sem, None, "Не удалось найти " + num_sem.__str__() + " семестр после выбора "
                                                                                              "второго направления!")

    def test_choosing_semesters_from_third_direction(self):
        self.page.choose_direction(3)
        nums_semesters = [1, 3]
        for num_sem in nums_semesters:
            choosing_sem = self.page.choose_sem(num_sem)
            self.assertNotEqual(choosing_sem, None, "Не удалось найти " + num_sem.__str__() + " семестр после выбора "
                                                                                              "третьего направления!")

    def test_choosing_semesters_from_fourth_direction(self):
        self.page.choose_direction(4)
        nums_semesters = [1, 3]
        for num_sem in nums_semesters:
            choosing_sem = self.page.choose_sem(num_sem)
            self.assertNotEqual(choosing_sem, None, "Не удалось найти " + num_sem.__str__() + " семестр после выбора "
                                                                                              "четвертого направления!")

    def test_input_id(self):
        input_value_id = "123"
        output_value_id = self.page.write_id(input_value_id)
        self.assertEqual(input_value_id, output_value_id, "Идентификатор был введен неверно!")

    def test_alert_choosing_sem(self):
        self.page.choose_direction(1)

        self.page = self.page.click_start_button_alert()

        self.assertNotEqual(self.page, None, "На кнопку для старта опроса не удалось нажать!")

        alert = self.page.find_alert()
        self.assertNotEqual(alert, None, "Не было найдено предупреждение о выборе семестра!")

        alert_text = alert.text
        expected_alert_text = "Пожалуйста, выберите семестр!"
        self.assertEqual(alert_text, expected_alert_text, "Текст предупреждения не соответствует ожидаемому!")

    def test_alert_filling_id(self):
        self.page.choose_direction(1)
        self.page.choose_sem(5)

        self.page = self.page.click_start_button_alert()

        self.assertNotEqual(self.page, None, "На кнопку для старта опроса не удалось нажать!")

        alert = self.page.find_alert()
        self.assertNotEqual(alert, None, "Не было найдено предупреждение об отсутствии идентификатора!")

        alert_text = alert.text
        expected_alert_text = 'Пожалуйста, заполните поле "Идентификатор"!'
        self.assertEqual(alert_text, expected_alert_text, "Текст предупреждения не соответствует ожидаемому!")

    def test_start_survey(self):
        self.page.choose_direction(1)
        self.page.choose_sem(5)

        input_value_id = "123"
        self.page.write_id(input_value_id)

        self.page = self.page.click_start_button_success()

        self.assertNotEqual(self.page, None, "На кнопку для старта опроса не удалось нажать!")

        current_url = self.driver.current_url
        expected_url = self.page.site_path + "semester/15123"
        self.assertEqual(current_url, expected_url, "Не удалось перейти на ожидаемую страницу опроса!")
