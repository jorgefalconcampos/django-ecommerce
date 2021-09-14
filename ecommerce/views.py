from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login, logout as do_logout
from django.shortcuts import redirect
from django.contrib import messages

TEMPLATES =  settings.TEMPLATES_DIR #importing templates path from Django settings

def index(request):
    """Main entry point of the app"""
    template_dir = TEMPLATES / 'main' / 'index.html'
    return render(request, template_dir, {'message': 'holaaaa'})


def login(request):
    """User login"""
    template_dir = TEMPLATES / 'user' / 'login.html'

    usr = request.POST.get('username')
    pwd  = request.POST.get('password')

    if request.method == 'POST':
        if usr or pwd:
            user_auth = authenticate(username=usr, password=pwd)

            if user_auth:
                do_login(request, user_auth)
                print(f"\nSession created for the user: {usr}\n")
                messages.success(request, f"Bienvenido {usr}")
                return redirect('index')
            else:
                print(f"No autenticado: {usr}")
                messages.error(request, "Usuario o contraseña inválidos")
        else:
            print("no autenticado (campos vacíos)")
    return render(request, template_dir, {})


def logout(request):
    """User logout"""
    do_logout(request)
    messages.success(request, 'Logged out')
    return redirect('login')

