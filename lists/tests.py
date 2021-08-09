from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from .models import Item, List


class ListViewTest(TestCase):
    """Тест списка дел"""

    def test_uses_list_template(self):
        response = self.client.get('/lists/unique_url/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/lists/unique_url/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new/', data={'item_text': 'A new list item'})
        new_items = Item.objects.all()
        self.assertEqual(new_items.count(), 1)
        self.assertEqual(new_items.first().text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new/', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/unique_url/')


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListandItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        self.assertEqual(list_, List.objects.first())

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
