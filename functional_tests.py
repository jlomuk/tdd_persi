import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    """тест нового посетителя"""

    def setUp(self) -> None:
        """Начальная конфигурация"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """Деструктор"""
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Можно начать новый список и получить его позже"""
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('FINISH TEST')


if __name__ == '__main__':
    unittest.main()
