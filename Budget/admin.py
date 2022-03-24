from django.contrib import admin

from Budget.models import Budget, Depense

# Register your models here.

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'owner', 'total', 'date',)
    search_field = ('titre', 'owner', 'total', 'date',)
    list_per_page = 5
    
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('designation', 'prix_unitaire', 'quantite', 'description', 'owner', 'budget', 'total', 'status',)
    search_field = ('designation', 'prix_unitaire', 'quantite', 'description', 'owner', 'budget', 'total', 'status',)
    list_per_page = 5
    
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Depense, DepenseAdmin)
