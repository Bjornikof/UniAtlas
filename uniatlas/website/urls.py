from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('resultpage/', views.resultpage),
    path('login/', views.login),
    path('login/signup/', views.signup),
    path('unisozluk/', views.unisozluk),
    path('unipage/', views.unipage),
    path('profile/', views.profile),
    path('unilist/', views.unilist),
    path('asistant/', views.asistant),

    path('userprofile/', views.userprofile)
]
