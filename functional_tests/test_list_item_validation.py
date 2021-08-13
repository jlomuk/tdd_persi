from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.assertEqual(
            self.wait_css_element('#id_text:invalid').text, ''
        )
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self._check_for_row_in_list_table('1: Buy milk')

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.assertEqual(
            self.wait_css_element('#id_text:invalid').text, ''
        )

        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self._check_for_row_in_list_table('1: Buy milk')
        self._check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_dublicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self._check_for_row_in_list_table('1: Buy wellies')

        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.assertEqual(
            self.wait_css_element('.has-error').text,
            'You have already got this in your list'
        )
