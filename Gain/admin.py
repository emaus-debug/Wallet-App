from django.contrib import admin
from .models import Income, Source

# Register your models here.

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'source', 'description', 'owner', 'date',)
    search_field = ('amount', 'source', 'description', 'date',)
    list_per_page = 5
admin.site.register(Income, IncomeAdmin)
admin.site.register(Source)