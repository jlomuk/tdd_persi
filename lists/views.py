from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from .forms import ItemForm, ExistingListItemForm, NewListForm
from .models import List


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
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(list_)
        return redirect(str(list_.get_absolute_url()))
    return render(request, 'home.html', {'form': form})


def new_list2(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def my_lists(request, email):
    User = get_user_model()
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
