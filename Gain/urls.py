from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="incomes"),
    path('create', views.create, name="create-incomes"),
    path('edit/<int:id>', views.edit, name="edit-income"),
    path('delete/<int:id>', views.delete, name="delete-income"),
    path('search', csrf_exempt(views.search), name="search-incomes"),
]