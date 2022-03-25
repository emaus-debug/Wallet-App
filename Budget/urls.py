from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="budgets"),
    path('show/<int:id>', views.show, name="show"),
    path('create', views.create, name="create-budgets"),
    path('create-elements', views.create_element, name="create-elements"),
    path('edit/<int:id>', views.edit, name="edit-budget"),
    path('delete/<int:id>', views.delete, name="delete-budget"),
    path('search', csrf_exempt(views.search), name="search-budgets"),
    path('search-element', csrf_exempt(views.search_element), name="search-budgets-elements"),
    path('edit-budget-element/<int:id>', views.edit_element, name="edit-budget-element"),
    path('delete-budget-element/<int:id>', views.delete_element, name="delete-budget-element"),
    path('export-excel-budget', views.export_excel, name="export-excel-budget"),
]