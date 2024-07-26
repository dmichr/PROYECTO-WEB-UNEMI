from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .models import Publicacion
from .forms import CustomUserCreationForm

from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def home(request):
    publicaciones = Publicacion.objects.filter(activo=True).order_by('-fecha_publicacion')
    return render(request, 'core/index.html', {'publicaciones': publicaciones})
    
    
def detalle_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion, id=id)
    if publicacion.html_contenido:
        with open(publicacion.html_contenido.path, 'r', encoding='utf-8') as file:
            html_contenido = file.read()
    else:
        html_contenido = publicacion.html_contenido
    return render(request, 'core/publicacion.html', {'publicacion': publicacion, 'html_contenido': html_contenido})


def about(request):
    return render(request, 'core/about.html')

def service(request):
    return render(request, 'core/service.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        message = request.POST.get('message')

        # Componer el mensaje de correo electrónico
        subject = f'Nueva consulta de {name}'
        email_message = (
            f'Nombre: {name}\n'
            f'Correo electrónico: {email}\n'
            f'Celular: {phone}\n'
            f'Tipo de Servicio: {service}\n\n'
            f'Mensaje:\n{message}'
        )

        # Enviar el correo al administrador
        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            ['dromeroo@unemi.edu.ec'],
            fail_silently=False,
        )

        return redirect('contact_success')  # Redirigir a una página de éxito

    return render(request, 'core/contact.html')


def contact_success(request):
    return render(request, 'contact_success.html')
    
    
    
    
    
    #return render(request, 'core/contact.html')

def login(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        if email and password1:
            user = authenticate(request, username=email, password=password1)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')  # Redirige al dashboard
            else:
                return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
        else:
            return render(request, 'login.html', {'error': 'Por favor completa todos los campos'})
    return render(request, 'login.html')






@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }
    print('se envió')
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        print('se esta validando')
        if user_creation_form.is_valid():
            print('se guardó')
            user_creation_form.save()
            print('se esta guardanando')
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            auth_login(request, user)
            return redirect('home')
        else:
            data['form'] = user_creation_form
            

    return render(request, 'registration/login.html', data)