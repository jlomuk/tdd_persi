from selenium import webdriver

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    """тест нового посетителя"""

    def test_can_start_a_list_for_one_user(self):
        """Можно начать новый список и получить его позже"""
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        self._input_new_item_in_table('Купить павлиньи перья')
        self._check_for_row_in_list_table('1: Купить павлиньи перья')
        self._input_new_item_in_table('Сделать мушку из павлиньих перьев')
        self._check_for_row_in_list_table(
            '2: Сделать мушку из павлиньих перьев')

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
        self._check_for_row_in_list_table(
            '1: Сделать мушку из павлиньих перьев')
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotEqual(francis_list_url, edith_list_url)
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Сделать мушку из павлиньих перьев', page_text)