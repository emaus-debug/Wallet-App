from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses
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

        expenses = Expenses.objects.filter(amount__istartswith = search_str, owner = request.user) | Expenses.objects.filter(date__istartswith = search_str, owner = request.user) | Expenses.objects.filter(description__icontains = search_str, owner = request.user) | Expenses.objects.filter(category__icontains = search_str, owner = request.user)
        data = expenses.values()

        return JsonResponse(list(data), safe=False)

@login_required(login_url = "/authapp/login")

def index(request):
    expenses = Expenses.objects.filter(owner = request.user).order_by('date')
    total = 0
    for expense in expenses:
        total += int(expense.amount)
    
    paginator = Paginator(expenses,4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user = request.user).currency
    except UserPreference.DoesNotExist:
        currency = None
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
        'total': total,
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

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days = 30*6)
    expenses = Expenses.objects.filter(owner = request.user, date__gte = six_months_ago, date__lte = todays_date)
    finalrep = {}
    
    def get_category(expense):
        return expense.category
    
    category_list = list(set(map(get_category, expenses)))
    
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category = category)
        for item in filtered_by_category:
            amount += int(item.amount)
        return amount
    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)
            
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def stats_view(request):
    return render(request,  'Depenses/stats.html')

# def export_csv(request):
#     response = HttpResponse(content_type = 'text/csv')
#     response['Content_Disposition'] = 'attachement; filename=Sortie d\'argent' + str(datetime.datetime.now()) + '.csv'
#     writer = csv.writer(response)
#     writer.writerow(['Montant', 'Category', 'Description', 'Date'])
#     expenses = Expenses.objects.filter(owner = request.user)
    
#     for expense in expenses:
#         writer.writerow([expense.amount, expense.category, expense.description, expense.date])
    
#     return response

def export_excel(request):
    response = HttpResponse(content_type = 'application/vnd.ms-excel')
    response['Content_Disposition'] = 'attachement; filename=Sortie d\'argent' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Montant', 'Category', 'Description', 'Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()
    rows = Expenses.objects.filter(owner = request.user).values_list('amount', 'category', 'description', 'date')
    
    for row in rows:
        row_num +=1
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
            
    wb.save(response)
    
    return response

# def export_pdf(request):
#     response = HttpResponse(content_type = 'application/pdf')
#     response['Content_Disposition'] = 'attachement; filename=Sortie d\'argent' + str(datetime.datetime.now()) + '.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'
    
#     html_string = render_to_string('Depenses/pdf-output.html', {'expense':[],'total': 0})
#     html = HTML(string = html_string)
#     result = html.write_pdf()
    
#     with tempfile.NamedTemporaryFile(delete = True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())
        
#     return response
    