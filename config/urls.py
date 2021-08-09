from django.contrib import admin
from django.urls import path

from lists import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home_page'),
    path('lists/unique_url/', views.view_list, name='view_list'),

]
