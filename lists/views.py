from django.shortcuts import render, redirect

from .models import Item

def home_page(request):
    """Домашняя страница"""
    if request.method == 'POST':
        Item.objects.create(text=request.POST.get('item_text', ''))
        return redirect('/')
    return render(request, 'home.html')
