from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Item, List
from .forms import ItemForm


def home_page(request):
    """Домашняя страница"""
    form = ItemForm()
    return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    """Выводит список дел и добавляет в этот список дел новые элементы"""
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST.get('item_text', ''), list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can not have an empty list item"
    return render(request, 'list.html', {'list': list_, 'error': error})


def new_list(request):
    """Создает новый список дел и добавляет запись"""
    list_ = List.objects.create()
    item = Item(text=request.POST.get('item_text', ''), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can not have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{list_.id}/')
