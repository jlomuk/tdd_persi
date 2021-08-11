from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request):
    """Домашняя страница"""
    return render(request, 'home.html')


def view_list(request, id):
    """Выводит список дел"""
    list_ = List.objects.get(id=id)
    items = list_.item_set.all()
    return render(request, 'list.html', {'items': items, 'list': list_})


def new_list(request):
    """Создает новый список дел и добавляет запись"""
    list_ = List.objects.create()
    item = Item(text=request.POST.get('item_text', ''), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{list_.id}/')


def add_item(request, id):
    """Добавляет запись в существующий список"""
    list_ = List.objects.get(id=id)
    Item.objects.create(text=request.POST.get('item_text', ''), list=list_)
    return redirect(f'/lists/{list_.id}/')