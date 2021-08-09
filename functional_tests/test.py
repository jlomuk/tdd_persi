import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    """тест нового посетителя"""

    def setUp(self) -> None:
        """Начальная конфигурация"""
        try:
            self.browser = webdriver.Firefox()
        except:
            self.browser = webdriver.Chrome()
            
    def tearDown(self) -> None:
        """Деструктор"""
        self.browser.quit()

    def _check_for_row_in_list_table(self, row_text):
        """Проверка нахождения строки  таблице шаблона"""
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def _input_new_item_in_table(self, item):
        """Ввод новых элементов в шаблон"""
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(item)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Можно начать новый список и получить его позже"""
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        self._input_new_item_in_table('Купить павлиньи перья')
        time.sleep(2)
        self._input_new_item_in_table('Сделать мушку из павлиньих перьев')
        time.sleep(2)
        self._check_for_row_in_list_table('1: Купить павлиньи перья')
        self._check_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

