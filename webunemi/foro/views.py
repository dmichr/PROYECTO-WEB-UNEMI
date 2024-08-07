from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.views.generic import ListView

from .models import Publicacion, Carrusell, Boletin, Evento

from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from django.db.models import Count
from django.db.models.functions import TruncDate
from itertools import groupby
from operator import attrgetter



# Create your views here.
class BoletinListView(ListView):
    model = Boletin
    template_name = 'core/lista_boletines.html'
    context_object_name = 'boletines_agrupados'
    paginate_by = 12 
     
    def get_queryset(self):
        queryset = Boletin.objects.all().order_by('-fecha')
        grouped=groupby(queryset, key=attrgetter('fecha'))
        result = []
        for fecha, boletines in grouped:
            result.append((fecha, list(boletines)))
        
        return result
    
def get_events(request):
    events = Evento.objects.all().values('title', 'start_date', 'end_date', 'description', 'location', 'url')
    events_list = list(events)
    for event in events_list:
        event['start'] = event.pop('start_date').isoformat()
        event['end'] = event.pop('end_date').isoformat()
    return JsonResponse({'events': events_list})
    
    
    
    





def home(request):
    publicaciones = Publicacion.objects.filter(activo=True)[:4]
    carrusell = Carrusell.objects.filter(activo=True).order_by('-fecha_subida')
    carrusell_length = len(carrusell)
    step = 100 / carrusell_length if carrusell_length > 0 else 0

    # Generar keyframes
    keyframes = []
    for i in range(carrusell_length):
        keyframes.append({
            'percent': step * i,
            'transform': f'translate3d(calc(-100% * {i}), 0, 0)'
        })

    last_index = carrusell_length - 1 if carrusell_length > 0 else 0

    context = {
        'publicaciones': publicaciones,
        'carrusell': carrusell,
        'carrusell_length': carrusell_length,
        'step': step,
        'keyframes': keyframes,
        'last_index': last_index
    }
    return render(request, 'core/index.html', context)

    
def detalle_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion, id=id)
    if publicacion.html_contenido:
        with open(publicacion.html_contenido.path, 'r', encoding='utf-8') as file:
            html_contenido = file.read()
    else:
        html_contenido = publicacion.html_contenido
    return render(request, 'core/publicacion.html', {'publicacion': publicacion, 'html_contenido': html_contenido})


def lista_publicaciones(request):
    publicaciones = Publicacion.objects.order_by('-fecha_publicacion')
    return render(request, 'core/lista_publicaciones.html', {'publicaciones': publicaciones})


def about(request):  
    
    return render(request,'core/about.html')


def all_events(request):                     
    all_events = Evento.objects.all()               
    out = []       
    for event in all_events: 
        out.append({      
            'id': event.id,  # Añadido ID para facilitar la identificación
            'title': event.title,          
            'description': event.description,
            'start': event.start_date.strftime("%Y-%m-%dT%H:%M:%S"),  # Formato ISO 8601
            'end': event.end_date.strftime("%Y-%m-%dT%H:%M:%S"),     # Formato ISO 8601
            'location': event.location,  # Incluye la ubicación si es necesario
            'url': event.get_absolute_url(),            # Incluye URL si es necesario
        })                      
    return JsonResponse(out, safe=False) 




'''def about(request):
    
    return render(request, 'core/about.html')'''

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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')

        elif 'register' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Cuenta creada para {username}. Ya puedes iniciar sesión.')
                return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'login.html', {'form': form})




@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

