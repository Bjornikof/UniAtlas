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
    path('assistant/', views.assistant),
    path('userprofile/', views.userprofile),
    path('uniedit/', views.uniedit),
    path('settings/', views.settings),
    path('settings2/', views.settings2),
    path('admin/controlpanel', views.controlpanel),
    path('admin/add/university', views.add_uni),
    path('admin/delete/university/<int:pk>', views.delete_uni),
    path('admin/edit/university/<int:pk>', views.edit_university),
    path('admin/add/faculty', views.add_faculty),
    path('admin/delete/faculty/<int:pk>', views.delete_faculty),
    path('admin/edit/faculty/<int:pk>', views.edit_faculty),
    path('admin/add/departmant', views.add_departmant),
    path('admin/edit/departmant/<int:pk>', views.edit_departmant),
    path('admin/delete/departmant/<int:pk>', views.delete_departmant)
]
