from django.shortcuts import render, redirect

from .models import List
from .forms import ItemForm, ExistingListItemForm


def home_page(request):
    """Домашняя страница"""
    form = ItemForm()
    return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    """Выводит список дел и добавляет в этот список дел новые элементы"""
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(data=request.POST, for_list=list_)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    """Создает новый список дел и добавляет запись"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(list_)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})

def my_lists(request, email):
    return render(request, 'my_lists.html')