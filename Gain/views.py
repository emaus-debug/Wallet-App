from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Source, Income
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

        incomes = Income.objects.filter(amount__istartswith = search_str, owner = request.user) | Income.objects.filter(date__istartswith = search_str, owner = request.user) | Income.objects.filter(description__icontains = search_str, owner = request.user) | Income.objects.filter(source__icontains = search_str, owner = request.user)
        data = incomes.values()

        return JsonResponse(list(data), safe=False)

@login_required(login_url = "/authapp/login")

def index(request):
    incomes = Income.objects.filter(owner = request.user).order_by('date')
    total = 0
    for income in incomes:
        total += int(income.amount)
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
        'total': total,
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

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days = 30*6)
    incomes = Income.objects.filter(owner = request.user, date__gte = six_months_ago, date__lte = todays_date)
    finalrep = {}
    
    def get_source(income):
        return income.source
    
    source_list = list(set(map(get_source, incomes)))
    
    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source = source)
        for item in filtered_by_source:
            amount += int(item.amount)
        return amount
    for x in incomes:
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)
            
    return JsonResponse({'income_source_data': finalrep}, safe=False)

def stats_view(request):
    return render(request,  'Gain/stats.html')

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
    response['Content_Disposition'] = 'attachement; filename = Entrée d\'argent' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Income')
    row_num = 0 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Montant', 'Source', 'Description', 'Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()
    rows = Income.objects.filter(owner = request.user).values_list('amount', 'source', 'description', 'date')
    
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
    