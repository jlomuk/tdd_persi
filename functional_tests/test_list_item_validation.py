import time

from unittest import skip
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        wait_css_element = FunctionalTest._wait_element(
            self.browser.find_element_by_css_selector
        )
        self.assertEqual(
            wait_css_element('#id_text:invalid').text, ''
        )
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self._check_for_row_in_list_table('1: Buy milk')

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.assertEqual(
            wait_css_element('#id_text:valid').text, ''
        )
 
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self._check_for_row_in_list_table('1: Buy milk')
        self._check_for_row_in_list_table('2: Make tea')
