from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'heustonn-html/index.html')

def about(request):
    return render(request, 'heustonn-html/about.html')

def service(request):
    return render(request, 'heustonn-html/service.html')

def contact(request):
    return render(request, 'heustonn-html/contact.html')
