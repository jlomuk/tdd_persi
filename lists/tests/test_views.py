import unittest
from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import reverse
from django.test import TestCase
from django.urls import resolve

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List
from lists.views import home_page, new_list2

User = get_user_model()


class ListViewTest(TestCase):
    """Тест списка дел"""

    def post_invalid_input(self):
        list_ = List.objects.create()
        response = self.client.post(
            reverse('view_list', args=[list_.id]),
            data={'item_text': ''}
        )
        return response

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        expected_error = "You can not have an empty list item"
        self.assertContains(response, expected_error)

    def test_invalid_list_arent_saved(self):
        self.client.post(reverse('new_list'), data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            reverse('view_list', args=[correct_list.id]),
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            reverse('view_list', args=[correct_list.id]),
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other item', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other item')

    def test_test_display_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(reverse('view_list', args=[list_.id]))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'}
        )
        expected_error = 'You have already got this in your list'
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.count(), 1)


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):

    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_obj = mock_form.save.return_value
        mock_obj.get_absolute_url.return_value = 'fake'

        new_list2(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        mock_obj = mock_form.save.return_value
        mock_obj.get_absolute_url.return_value = 'fake'

        new_list2(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
            self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list2(self.request)
        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(
            self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        response = new_list2(self.request)

        self.assertEqual(response, mock_render.return_value)

        mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form}
        )
    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        response = new_list2(self.request)
        self.assertFalse(mock_form.save.called)



class NewListIntegratedTest(TestCase):

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post(reverse('new_list'), data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post(reverse('new_list'), data={'text': ''})
        expected_error = "You can not have an empty list item"
        self.assertContains(response, expected_error)

    def test_validation_input_passes_form_to_template(self):
        response = self.client.post(reverse('new_list'), data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_can_save_a_POST_request(self):
        response = self.client.post(reverse('new_list'), data={
            'text': 'A new list item'})
        new_items = Item.objects.all()
        self.assertEqual(new_items.count(), 1)
        self.assertEqual(new_items.first().text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(reverse('new_list'), data={
            'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    @unittest.skip
    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new/', data={'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


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

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class MyListTest(TestCase):

    def test_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com')
        self.assertEqual(response.context['owner'], correct_user)
