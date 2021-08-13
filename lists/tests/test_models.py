from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from lists.models import Item, List


class ItemTest(TestCase):

    def test_dafault_text(self):
        item = Item()
        self.assertEqual(item.text, '')


class ListTest(TestCase):

    def test_can_not_save_empty_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_dublicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(IntegrityError):
            item = Item(list=list_, text='bla')
            item.full_clean
            item.save()

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()

