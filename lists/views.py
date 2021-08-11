from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Item, List


def home_page(request):
    """Домашняя страница"""
    return render(request, 'home.html')


def view_list(request, list_id):
    """Выводит список дел"""
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST.get('item_text', ''), list=list_)
        return redirect(reverse('view_list', args=[list_.id]))
    return render(request, 'list.html', {'list': list_})


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