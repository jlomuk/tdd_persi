from django.shortcuts import render, redirect

from .models import Item


def home_page(request):
    """Домашняя страница"""
    return render(request, 'home.html')


def view_list(request):
    """Выводит список дел"""
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    """Создает новую запись в списке дел"""
    Item.objects.create(text=request.POST.get('item_text', ''))
    return redirect('/lists/unique_url/')