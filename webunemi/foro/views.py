from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Usuario
# Create your views here.


def home(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def service(request):
    return render(request, 'core/service.html')

def contact(request):
    return render(request, 'core/contact.html')

def login(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')  # Redirige al dashboard
            else:
                return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
        else:
            return render(request, 'login.html', {'error': 'Por favor completa todos los campos'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index.html')

def register_view(request):
    if request.method == 'POST':
        nombre = request.POST.get ('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        usuario = email.split('@')[0]

        # Verificar si el correo ya está registrado
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'login.html', {'error': 'El correo ya está registrado'})
        
        # Crear un nuevo usuario
        Usuario.objects.create(
            nombre=nombre,
            email=email,
            usuario=usuario,
            contraseña=make_password(password)  # Encripta la contraseña
        )
        return redirect('login')  # Redirige a la página de inicio de sesión
    return render(request, 'login.html')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')