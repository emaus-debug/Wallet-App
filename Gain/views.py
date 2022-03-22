from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

# Create your views here.

def search(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        incomes = Income.objects.filter(amount__istartswith = search_str, owner = request.user) | Income.objects.filter(date__istartswith = search_str, owner = request.user) | Income.objects.filter(description__icontains = search_str, owner = request.user) | Income.objects.filter(source__icontains = search_str, owner = request.user)
        data = incomes.values()

        return JsonResponse(list(data), safe=False)

@login_required(login_url = "/authapp/login")

def index(request):
    sources = Source.objects.all()
    incomes = Income.objects.filter(owner = request.user)
    paginator = Paginator(incomes,4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user = request.user).currency
    except UserPreference.DoesNotExist:
        currency = None
    context = {
        'incomes': incomes,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'Gain/index.html', context)

def create(request):
    sources = Source.objects.all()
    context ={
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET' :
        return render(request, 'Gain/create.html', context)

    if request.method == 'POST' :
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, "Merci de rensigner le montant avant de valider")
            return render(request, 'Gain/create.html', context)

        if not description:
            messages.error(request, "Merci de rensigner la description avant de valider")
            return render(request, 'Gain/create.html', context)

        Income.objects.create(owner = request.user ,amount = amount, description = description, date = date, source = source)
        messages.success(request, 'Enregistré avec succès')
        return redirect('incomes')


@login_required(login_url = "/authapp/login")

def edit(request, id):
    income = Income.objects.get(pk = id)
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'income': income,
        'values': income,
    }
    if request.method == "GET":
        
        return render(request, "Gain/edit.html", context)
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, "Merci de rensigner le montant avant de valider")
            return render(request, 'Gain/create.html', context)

        if not description:
            messages.error(request, "Merci de rensigner la description avant de valider")
            return render(request, 'Gain/create.html', context)

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.description = description
        income.source = source
        income.save()
        messages.success(request, 'Mise à jour réussie')
        return redirect('incomes')
    

def delete(request, id):
    income = Income.objects.get(pk = id)
    income.delete()
    messages.success(request,"Supprimé avec succès")
    return redirect("incomes")