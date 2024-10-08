"""
URL configuration for webunemi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from foro.views import *
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # URL raíz
    path('boletines/', include('foro.urls')),
    path('about.html/', about, name='about'),
    path('all_events/', all_events, name='all_events'),
    path('service.html/', service, name='service'),
    path('contact.html/', contact, name='contact'),
    path('contact/success/', contact_success, name='contact_success'),
    path('', include('user.urls')),
    path('dashboard.html/', dashboard, name='dashboard'),
    
    path('publicacion/<int:id>/', detalle_publicacion, name='detalle_publicacion'),
    path('publicaciones/', lista_publicaciones, name='lista_publicaciones'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header = 'Odeme- administracion'

admin.site.index_title = 'Usuarios'
admin.site.site_title = 'ODEME'