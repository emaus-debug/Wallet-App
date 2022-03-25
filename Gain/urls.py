from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="incomes"),
    path('create', views.create, name="create-incomes"),
    path('edit/<int:id>', views.edit, name="edit-income"),
    path('delete/<int:id>', views.delete, name="delete-income"),
    path('search', csrf_exempt(views.search), name="search-incomes"),
    path('income_source_summary', views.income_source_summary, name="income_source_summary"),
    path('stats', views.stats_view, name="stats-income"),
    # path('export-csv', views.export_csv, name="export-csv"),
    # path('export-pdf', views.export_pdf, name="export-pdf"),
    path('export-excel-gain', views.export_excel, name="export-excel-gain"),
]