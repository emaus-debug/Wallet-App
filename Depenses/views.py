from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url = "/authapp/login")

def index(request):
    return render(request, 'Depenses/index.html')

def create(request):
    return render(request, 'Depenses/create.html')