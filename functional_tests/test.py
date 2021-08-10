import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


def wait_element(func):
    MAX_WAIT = 5
    def wraper(*args, **kwargs):
        start = time.time()
        while True:
            try:
                func(*args, *kwargs)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return wraper


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

    @wait_element
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

    def test_can_start_a_list_for_one_user(self):
        """Можно начать новый список и получить его позже"""
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        self._input_new_item_in_table('Купить павлиньи перья')
        self._check_for_row_in_list_table('1: Купить павлиньи перья')
        self._input_new_item_in_table('Сделать мушку из павлиньих перьев')
        self._check_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        self._input_new_item_in_table('Купить павлиньи перья')
        self._check_for_row_in_list_table('1: Купить павлиньи перья')
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.browser.quit()
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)
        self._input_new_item_in_table('Сделать мушку из павлиньих перьев')
        self._check_for_row_in_list_table('1: Сделать мушку из павлиньих перьев')
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotEqual(francis_list_url, edith_list_url)
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Сделать мушку из павлиньих перьев', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        _check_for_row_in_list_table('1: testing')

        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        