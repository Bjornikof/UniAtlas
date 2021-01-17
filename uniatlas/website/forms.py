from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from .models import University, Faculties, Department, SCHOLARSHIP_CHOICES

User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)


class UniForm(forms.ModelForm):
    image = forms.ImageField(label='', required=False)
    class Meta:
        model = University
        fields = [
            'image',
            'name',
            'city',
            'history',
            'types'
        ]


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculties
        fields = [
            'university',
            'name',
            'edu_field'
        ]


class DepartForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'faculty',
            'name',
            'scholarship',
            'total_year',
            'score'
        ]

