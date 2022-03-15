from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="expenses"),
    path('create', views.create, name="create-expenses"),
    path('edit/<int:id>', views.edit, name="edit-expense"),
    path('delete/<int:id>', views.delete, name="delete-expense"),
]