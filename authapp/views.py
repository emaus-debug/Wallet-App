import email
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email

# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error' : 'Email invalid ' }, status=400)
        if User.objects.filter(email = email).exists() : 
            return JsonResponse({'email_error' : 'Désolé cet email est déja utilisé, veuillez en choisir un autre'}, status=409)

        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'Le nom d\'utilisateur doit contenir uniquement que des caractères alphanumérique' }, status=400)
        if User.objects.filter(username = username).exists() : 
            return JsonResponse({'username_error' : 'Désolé cet nom d\'utilisateur existe déjà veuillez en choisir un autre'}, status=409)

        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authapp/register.html')