from unittest import skip
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        wait_css_element = FunctionalTest._wait_element(
            self.browser.find_element_by_css_selector)
        self.assertEqual(
            wait_css_element('.has-error').text,
            "You can't have an empty list item"
        )
