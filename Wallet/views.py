from django.shortcuts import redirect, render
from Depenses.views import Expenses
from Gain.views import Income

def index(request):
    expenses = Expenses.objects.filter(owner = request.user)
    incomes = Income.objects.filter(owner = request.user)
    total_expense = 0
    for expense in expenses:
        total_expense += int(expense.amount)
    total_income = 0
    for income in incomes:
        total_income += int(income.amount)

    caisse = total_income - total_expense
    context = {
        'caisse': caisse,
        'total_expense': total_expense,
        'total_income': total_income,
    }
    return render(request, 'resume.html', context)