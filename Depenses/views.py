from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url = "/authapp/login")

def index(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner = request.user)
    paginator = Paginator(expenses,2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
    }
    return render(request, 'Depenses/index.html', context)

def create(request):
    categories = Category.objects.all()
    context ={
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET' :
        return render(request, 'Depenses/create.html', context)

    if request.method == 'POST' :
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, "Merci de rensigner le montant avant de valider")
            return render(request, 'Depenses/create.html', context)

        if not description:
            messages.error(request, "Merci de rensigner la description avant de valider")
            return render(request, 'Depenses/create.html', context)

        Expenses.objects.create(owner = request.user ,amount = amount, description = description, date = date, category = category)
        messages.success(request, 'Enregistré avec succès')
        return redirect('expenses')

def edit(request, id):
    expense = Expenses.objects.get(pk = id)
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'expense': expense,
        'values': expense,
    }
    if request.method == "GET":
        
        return render(request, "Depenses/edit.html", context)
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, "Merci de rensigner le montant avant de valider")
            return render(request, 'Depenses/create.html', context)

        if not description:
            messages.error(request, "Merci de rensigner la description avant de valider")
            return render(request, 'Depenses/create.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.category = category
        expense.save()
        messages.success(request, 'Mise à jour réussie')
        return redirect('expenses')
    

def delete(request, id):
    expense = Expenses.objects.get(pk = id)
    expense.delete()
    messages.success(request,"Sipprimé avec succès")
    return redirect("expenses")