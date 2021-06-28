from start_page import start_page
from selenium.webdriver import Chrome
import random

import unittest


def is_unique_elements_in_array(arr):
    n = len(arr)
    repeats = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                repeats.append(arr[i])
    if len(repeats) == 0:
        return True
    else:
        return False


class test_survey_page(unittest.TestCase):
    season = "autumn"
    driver = Chrome()
    page = start_page(driver, season)
    driver.get(page.site_path)

    def tearDown(self):
        self.page = start_page(self.driver, self.season)
        self.driver.get(self.page.site_path)

    def choose_direction_and_semester(self, direction, semester):
        choosing_direction = self.page.choose_direction(direction)
        self.assertNotEqual(choosing_direction, None, "Не удалось найти " + direction.__str__() + " направление!")
        choosing_sem = self.page.choose_sem(semester)
        self.assertNotEqual(choosing_sem, None, "Не удалось найти " + semester.__str__() + " семестр после выбора "
                            + direction.__str__() +
                            " направления!")
        input_value_id = "123"
        value_id = self.page.write_id(input_value_id)
        self.assertEqual(input_value_id, value_id, "Идентификатор был введен неверно!")
        self.page = self.page.click_start_button_success()
        self.assertNotEqual(self.page, None, "На кнопку для старта опроса не удалось нажать!")

    def validation_survey_alert(self, direction, semester):
        self.choose_direction_and_semester(direction, semester)

        self.page = self.page.click_finish_button_alert()
        self.assertNotEqual(self.page, None, "На кнопку для старта опроса не удалось нажать!")

        alert = self.page.find_alert()
        self.assertNotEqual(alert, None, "Не было найдено предупреждение о выборе семестра!")

        alert_text = alert.text
        expected_alert_text = 'Обязательные поля не заполнены'
        self.assertEqual(alert_text, expected_alert_text, "Текст предупреждения не соответствует ожидаемому!")

    def validation_survey_success(self, direction, semester):
        self.choose_direction_and_semester(direction, semester)

        teachers_and_subjects = []
        error = False
        while self.page.go_to_next_teacher() is not None and error is False:
            teacher_and_subject = [self.page.current_name_teacher, self.page.current_subject]

            try:
                teachers_and_subjects.index(teacher_and_subject)
            except ValueError:
                teachers_and_subjects.append(teacher_and_subject)
            else:
                error = True

        self.assertEqual(error, False,
                         "После выбора " + direction.__str__() +
                         " направления и " + semester.__str__() + " семестра было обнаружено повторение имени - "
                         + teacher_and_subject[0] + ", ведущего " + teacher_and_subject[1])

        self.tearDown()

        self.choose_direction_and_semester(direction, semester)

        while self.page.go_to_next_teacher() is not None:
            type_rating = 'relevance'
            if self.page.is_compulsory_rating_current_subject(type_rating) is True:
                input_rating = random.randint(1, 5)
                rating_relevance = self.page.choose_rating_relevance(input_rating)
                self.assertNotEqual(rating_relevance, None, "После выбора " + direction.__str__() +
                                    " направления и " + semester.__str__() + " семестра не удалось выставить оценку "
                                                                             "актуальности преподавателю " +
                                    self.page.current_name_teacher + ", ведущего предмет " + self.page.current_subject
                                    + "!")

            type_rating = 'quality'
            if self.page.is_compulsory_rating_current_subject(type_rating) is True:
                input_rating = random.randint(1, 5)
                rating_quality = self.page.choose_rating_quality(input_rating)
                self.assertNotEqual(rating_quality, None, "После выбора " + direction.__str__() +
                                    " направления и " + semester.__str__() + " семестра не удалось выставить оценку "
                                                                             "качества преподавателю " +
                                    self.page.current_name_teacher + ", ведущего предмет " + self.page.current_subject
                                    + "!")

        self.page = self.page.click_finish_button_success()
        self.assertNotEqual(self.page, None, "На кнопку для завершения опроса не удалось нажать!")

        expected_finish_text = "Спасибо за участие в опросе!"
        finish_text = self.page.get_final_text()
        self.assertEqual(finish_text, expected_finish_text, "Текст окончания опроса не соответствует ожидаемому!")

    def validation_survey_menu(self, direction, semester):
        self.choose_direction_and_semester(direction, semester)
        teachers = []
        next_teacher = self.page.go_to_next_teacher_in_menu()
        while next_teacher is not None:
            teachers.append(next_teacher)
            next_teacher = self.page.go_to_next_teacher_in_menu()

        self.assertEqual(is_unique_elements_in_array(teachers), True, "В меню были обнаружены повторяющиеся имена "
                                                                      "преподавателей!")

    def test_validation_survey_success_all(self):
        count_directions = self.page.count_directions()
        for direction in range(1, count_directions + 1):
            semesters = self.page.semesters_from_direction(direction)
            for sem in semesters:
                self.validation_survey_success(direction, sem)
                self.tearDown()

    def test_validation_survey_alert_all(self):
        count_directions = self.page.count_directions()
        for direction in range(1, count_directions + 1):
            semesters = self.page.semesters_from_direction(direction)
            for sem in semesters:
                self.validation_survey_alert(direction, sem)
                self.tearDown()

    def test_validation_survey_menu_all(self):
        count_directions = self.page.count_directions()
        for direction in range(1, count_directions + 1):
            semesters = self.page.semesters_from_direction(direction)
            for sem in semesters:
                self.validation_survey_menu(direction, sem)
                self.tearDown()