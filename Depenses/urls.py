from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="expenses"),
    path('create', views.create, name="create-expenses"),
    path('edit/<int:id>', views.edit, name="edit-expense"),
    path('delete/<int:id>', views.delete, name="delete-expense"),
    path('search', csrf_exempt(views.search), name="search-expenses"),
    path('expense_category_summary', views.expense_category_summary, name="expense_category_summary"),
    path('stats', views.stats_view, name="stats"),
    # path('export-csv', views.export_csv, name="export-csv"),
    # path('export-pdf', views.export_pdf, name="export-pdf"),
    path('export-excel-depense', views.export_excel, name="export-excel-depense"),
]