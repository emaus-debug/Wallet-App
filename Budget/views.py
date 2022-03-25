from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Budget, Depense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
import csv
import xlwt

# Create your views here.

def search(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        budgets = Budget.objects.filter(titre__icontains = search_str, owner = request.user) | Budget.objects.filter(total__istartswith = search_str, owner = request.user) | Budget.objects.filter(date__istartswith = search_str, owner = request.user)
        data = budgets.values()

        return JsonResponse(list(data), safe=False)
    
def search_element(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        depenses = Depense.objects.filter(designation__icontains = search_str, owner = request.user) |Depense.objects.filter(description__icontains = search_str, owner = request.user) | Depense.objects.filter(prix_unitaire__istartswith = search_str, owner = request.user) | Depense.objects.filter(quantite__istartswith = search_str, owner = request.user) | Depense.objects.filter(total__istartswith = search_str, owner = request.user) | Depense.objects.filter(status__icontains = search_str, owner = request.user)
        data = depenses.values()

        return JsonResponse(list(data), safe=False)

@login_required(login_url = "/authapp/login")

def index(request):
    depenses = Depense.objects.filter(owner = request.user)
    budgets = Budget.objects.filter(owner = request.user)
    paginator = Paginator(budgets,4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user = request.user).currency
    except UserPreference.DoesNotExist:
        currency = None
    context = {
        'depenses': depenses,
        'budgets': budgets,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'Budget/index.html', context)

def show(request, id):
    depenses = Depense.objects.filter(owner = request.user)
    budget = Budget.objects.get(id = id)
    paginator = Paginator(depenses,4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user = request.user).currency
    except UserPreference.DoesNotExist:
        currency = None
    context = {
        'depenses': depenses,
        'budget': budget,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'Budget/show.html', context)

def create(request):
    context ={
        'values': request.POST
    }
    if request.method == 'GET' :
        return render(request, 'Budget/create.html', context)

    if request.method == 'POST' :
        titre = request.POST['titre']
        date = request.POST['budget_date']

        if not titre:
            messages.error(request, "Merci de rensigner le titre avant de valider")
            return render(request, 'Budget/create.html', context)
        
        total = 0

        Budget.objects.create(owner = request.user ,titre = titre, date = date, total = total )
        messages.success(request, 'Budget crée avec succès, ajoutez maintenant des éléments')
        return redirect('create-elements')
    
def create_element(request):
    budgets = Budget.objects.all()
    context ={
        'values': request.POST,
        'budgets': budgets
    }
    if request.method == 'GET' :
        return render(request, 'Budget/create-element.html', context)

    if request.method == 'POST' :
        designation = request.POST['designation']
        prix_unitaire = request.POST['prix_unitaire']
        description = request.POST['description']
        quantite = request.POST['quantite']
        budget = request.POST['budget']

        if not designation:
            messages.error(request, "Merci de rensigner la désignation avant de valider")
            return render(request, 'Budget/create-element.html', context)
        
        if not prix_unitaire:
            messages.error(request, "Merci de rensigner le prix unitaire avant de valider")
            return render(request, 'Budget/create-element.html', context)

        if not quantite:
            messages.error(request, "Merci de rensigner la quantite avant de valider")
            return render(request, 'Budget/create-element.html', context)

        if not description:
            messages.error(request, "Merci de rensigner la description avant de valider")
            return render(request, 'Budget/create-element.html', context)
        
        total = int(prix_unitaire) * int(quantite)
        
        elt = Budget.objects.get(id = budget)
        elt.total = total + int(elt.total)
        elt.save()
        elt2 = Budget.objects.get(id = budget)
        

        Depense.objects.create(owner = request.user ,designation = designation, prix_unitaire = prix_unitaire, description = description, quantite = quantite, total = total, budget = elt )
        messages.success(request, 'Enregistré avec succès')
        return redirect('budgets')
    
@login_required(login_url = "/authapp/login")

def edit(request, id):
    budget = Budget.objects.get(pk = id)
    context = {
        'budget': budget,
        'values': budget,
    }
    if request.method == "GET":
        
        return render(request, "Budget/edit.html", context)
    if request.method == "POST":
        designation = request.POST['designation']
        prix_unitaire = request.POST['prix_unitaire']
        description = request.POST['description']
        date = request.POST['budget_date']
        quantite = request.POST['quantite']

        if not designation:
            messages.error(request, "Merci de rensigner la désignation avant de valider")
            return render(request, 'Budget/edit.html', context)
        
        if not prix_unitaire:
            messages.error(request, "Merci de rensigner le prix unitaire avant de valider")
            return render(request, 'Budget/edit.html', context)

        if not quantite:
            messages.error(request, "Merci de rensigner la quantite avant de valider")
            return render(request, 'Budget/edit.html', context)

        if not description:
            messages.error(request, "Merci de rensigner la description avant de valider")
            return render(request, 'Budget/edit.html', context)

        total = int(prix_unitaire) * int(quantite)
        budget.owner = request.user
        budget.designation = designation
        budget.prix_unitaire = prix_unitaire
        budget.date = date
        budget.description = description
        budget.quantite = quantite
        budget.total = total
        budget.save()
        messages.success(request, 'Mise à jour réussie')
        return redirect('budgets')
    
def edit_element(request, id):
    budget = Budget.objects.get(pk = id)
    context = {
        'budget': budget,
        'values': budget,
    }
    if request.method == "GET":
        
        return render(request, "Budget/edit-element.html", context)
    if request.method == "POST":
        designation = request.POST['designation']
        prix_unitaire = request.POST['prix_unitaire']
        description = request.POST['description']
        date = request.POST['budget_date']
        quantite = request.POST['quantite']

        if not designation:
            messages.error(request, "Merci de rensigner la désignation avant de valider")
            return render(request, 'Budget/edit-element.html', context)
        
        if not prix_unitaire:
            messages.error(request, "Merci de rensigner le prix unitaire avant de valider")
            return render(request, 'Budget/edit-element.html', context)

        if not quantite:
            messages.error(request, "Merci de rensigner la quantite avant de valider")
            return render(request, 'Budget/edit-element.html', context)

        if not description:
            messages.error(request, "Merci de rensigner la description avant de valider")
            return render(request, 'Budget/edit-element.html', context)

        total = int(prix_unitaire) * int(quantite)
        budget.owner = request.user
        budget.designation = designation
        budget.prix_unitaire = prix_unitaire
        budget.date = date
        budget.description = description
        budget.quantite = quantite
        budget.total = total
        budget.save()
        messages.success(request, 'Mise à jour réussie')
        return redirect('budgets')

def delete(request, id):
    budget = Budget.objects.get(pk = id)
    budget.delete()
    messages.success(request,"Budget supprimé avec succès")
    return redirect("budgets")

def delete_element(request, id):
    depense = Depense.objects.get(pk = id)
    depense.delete()
    messages.success(request,"Element du Budget supprimé avec succès")
    return redirect("budgets")

def export_excel(request):
    response = HttpResponse(content_type = 'application/vnd.ms-excel')
    response['Content_Disposition'] = 'attachement; filename = Budget' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Budget')
    row_num = 0 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Designation', 'Prix Unitaire', 'Quantite', 'Description', 'Total', 'Statut']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()
    rows = Depense.objects.filter(owner = request.user).values_list('designation', 'prix_unitaire', 'quantite', 'description', 'total', 'status')
    
    for row in rows:
        row_num +=1
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
            
    wb.save(response)
    
    return response