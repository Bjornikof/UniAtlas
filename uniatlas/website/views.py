from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'website/home.html')


def login(request):
    return render(request, 'website/login.html')


def signup(request):
    return render(request, 'website/signup.html')


def unisozluk(request):
    return render(request, 'website/unisozluk.html')


def resultpage(request):
    return render(request, 'website/resultpage.html')

def unipage(request):
    return render(request, 'website/unipage.html')