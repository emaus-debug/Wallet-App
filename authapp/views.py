from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
# from django.core.mail import EmailMessage
from django.contrib import auth
# from django.urls import reverse
# from .utils import token_generator
# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.contrib.sites.shortcuts import get_current_site

import threading

# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send(fail_silently = False)

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
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST 
        }

        if not User.objects.filter(username = username).exists():
            if not User.objects.filter(email = email).exists():
                if len(password) < 6:
                    messages.error(request, 'Mot de Pass trop court')
                    return render(request, 'authapp/register.html', context)
                
                user = User.objects.create_user(username = username, email = email)
                user.set_password(password)
                # user.is_active = False
                user.save()

                # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                # domain = get_current_site(request).domain
                # link = reverse('activate', kwargs={'uidb64':uidb64, 'token': token_generator.make_token(user)})
                # activate_url = 'http://'+ domain + link

                # email_subject = 'Activation du compte'
                # email_body = "Salut"+ user.username +" "+ "Utilisez le lien suivant pour activer votre compte\n" + activate_url
                # email = EmailMessage(
                #     email_subject,
                #     email_body,
                #     'noreply@gmail.com',
                #     [email],
                # )
                # EmailThread(email).start()
                messages.success(request, 'Compte crée avec succès')
                return render(request, 'authapp/login.html')

        return render(request, 'authapp/register.html')

# class VerificationView(View):
#     def get(self, request, uidb64, token):

#         try:
#             id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=id)

#             if not account_activation_token.check_token(user, token):
#                 return redirect('login'+'?message='+'Utilisateur déjà activé')

#             if user.is_activate:
#                 return redirect('login')
                
#             user.is_active = True
#             user.save()

#             messages.success(request, "Compte activé avec succès")
#             return redirect('login')

#         except Exception as ex:
#             pass

#         return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, "authapp/login.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username = username, password = password)

            if user:
                auth.login(request, user)
                messages.success(request, "Bienvenu, " + user.username + ". Vous êtes maintenant connecté à votre compte")
                return redirect("expenses")

            messages.error(request, "Informations d'identification invalides, essayez à nouveau")
            return render(request, "authapp/login.html")
        messages.error(request, "Renseignez tous les champs s'il vous plait")
        return render(request, "authapp/login.html")

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "Vous êtes déconnecté")
        return redirect("login")
    
    
# class RequestPasswordResetEmail(View):
#     def get(self, request):
#         return render(request, "authapp/reset-password.html")
    
#     def post(self, request):
#         email = request.POST['email']
        
#         context = {
#             'values': request.POST
#         }
#         if not validate_email(email):
#                 messages.error(request, "Veuillez entrer un email valide")
#                 return render(request, "authapp/reset-password.html", context)
                
#         user = request.objects.filter(email = email)
        
#         if user.exists():
#             uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
#             domain = get_current_site(request).domain
#             link = reverse('set-new-password', kwargs={'uidb64':uidb64, 'token': PasswordResetTokenGenerator().make_token(user[0])})
#             reset_url = 'http://'+ domain + link

#             email_subject = 'Réinitialisation du mot de pass'
#             email_body = "Salut, Utilisez le lien suivant pour Réinitialiser votre mot de pass\n" + reset_url
#             email = EmailMessage(
#                 email_subject,
#                 email_body,
#                 'noreply@gmail.com',
#                 [email],
#             )
#             EmailThread(email).start()
            
#         messages.success(request, "Nous vous avons envoyé un mail pour réinitialiser votre mot de pass")
        
#         return render(request, "authapp/reset-password.html")
    

# class CompletePasswordReset(View):
#     def get(self, request, uidb64, token):
#         context = {
#             'uidb64': uidb64,
#             'token': token
#         }
        
#         try:
#             user_id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=user_id)
            
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 messages.info(request, "Lien invalid")
#                 return render(request, "authapp/reset-password.html")
#         except Exception as identifier:
#             pass
        
#         return render (request, "authapp/set-newpassword.html", context)
    
#     def post(self, request, uidb64, token):
#         context = {
#             'uidb64': uidb64,
#             'token': token
#         }
        
#         password = request.POST['password']
#         password2 = request.POST['password2']
        
#         if password != password2 :
#             messages.error(request, "Les mots de pass ne correspondent pas, veuillez réessayer ")
#             return render (request, "authapp/set-newpassword.html", context)
        
#         if len(password) < 6 :
#             messages.error(request, "Mot de pass trop court ")
#             return render (request, "authapp/set-newpassword.html", context)
        
#         try:
#             user_id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=user_id)
#             user.password = password
#             user.save()
            
#             messages.success(request, "Mot de pass modifié avec succès, vous pouvez vous connecter avec votre nouveau mot de pass")
#             return redirect('login')
#         except Exception as identifier:
#             messages.info(request, "Une erreur s'est produite, veuillez réessayer")
#             return render (request, "authapp/set-newpassword.html", context)
        
        
#         return render (request, "authapp/set-newpassword.html", context)
        