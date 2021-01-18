from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    get_user_model,

)
from .models import University, Faculties, Department, SCHOLARSHIP_CHOICES, TOTAL_YEAR_CHOICES, EDU_FIELD_CHOICES

User = get_user_model()


class CreateUserForm(UserCreationForm):
    EDU_CHOICES = [('Eğitim',(('1','Lise'),('1','Üniversite'),('1','Mezun'),))];
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'placeholder':'Kullanıcı Adı'}))
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    education = forms.ChoiceField(widget=forms.Select, choices=EDU_CHOICES, )
    password1 = forms.CharField(label='password1', widget=forms.PasswordInput(attrs={'placeholder': 'Şifre'}))
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput(attrs={'placeholder': 'Şifre(Tekrar)'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'education', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = False
        self.fields['email'].label = False
        self.fields['education'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False


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

class searchbyuni(forms.Form):
    search_key = forms.CharField()


class UniSearchForm(forms.Form):
    total_year = forms.ChoiceField(label='Türü', choices=TOTAL_YEAR_CHOICES, required=False)
    university = forms.ModelChoiceField(label='Üniversite', queryset=University.objects.all(), required=False)
    scholarship = forms.MultipleChoiceField(label='Burs Tipi', choices=SCHOLARSHIP_CHOICES, required=False)
    score = forms.FloatField(label='Puan', required=False)
    edu_field = forms.ChoiceField(label='Alan', choices=EDU_FIELD_CHOICES, required=False)
    city = forms.MultipleChoiceField(label='Şehir', choices=[], required=False)
    
    def __init__(self, *args, **kwargs):
        super(UniSearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].choices = University.objects.values_list('city', 'city').distinct()
