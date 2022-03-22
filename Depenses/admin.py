from django.contrib import admin
from .models import Expenses, Category

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'description', 'owner', 'date',)
    search_field = ('amount', 'category', 'description', 'date',)
    list_per_page = 5
admin.site.register(Expenses, ExpenseAdmin)
admin.site.register(Category)
