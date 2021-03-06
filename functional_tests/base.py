import time

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        """Начальная конфигурация"""
        self.browser = webdriver.Chrome()
        if settings.STAGING_SERVER:
            self.live_server_url = 'http://' + settings.STAGING_SERVER

    def tearDown(self) -> None:
        """Деструктор"""
        self.browser.quit()

    def _wait_element(func):
        """Декоратор для ожидания отображения элемента"""
        MAX_WAIT = 3 
        def wraper(*args, **kwargs):
            start = time.time()
            while True:
                try:
                    return func(*args, *kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return wraper

    @_wait_element
    def _check_for_row_in_list_table(self, row_text):
        """Проверка нахождения строки  таблице шаблона"""
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def _input_new_item_in_table(self, item):
        """Ввод новых элементов в шаблон"""
        inputbox = self.get_item_input_box()
        inputbox.send_keys(item)
        inputbox.send_keys(Keys.ENTER)

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def wait_css_element(self, selector):
        return FunctionalTest._wait_element(
            self.browser.find_element_by_css_selector)(selector)

    def wait_tag_element(self, tag):
        return FunctionalTest._wait_element(
            self.browser.find_element_by_tag_name)(tag)

    def wait_link_text_element(self, link):
        return FunctionalTest._wait_element(
            self.browser.find_element_by_link_text)(link)

    def wait_name_element(self, name):
        return FunctionalTest._wait_element(
            self.browser.find_element_by_name)(name)

    def wait_to_be_logged_in(self, email):
        self.wait_link_text_element('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_name_element('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
