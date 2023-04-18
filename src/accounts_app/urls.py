from django.contrib import admin
from django.urls import path

from accounts_app.views import login_view, logout_view, register_view

urlpatterns = [
    path('login/', login_view, name='login'),  # name - наименование относительной ссылки
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]
