from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.defaultfilters import register
import logging

from .models import Enrolee, Admin, University, Faculties, Department, SCHOLARSHIP_CHOICES
from .forms import UniForm, FacultyForm, DepartForm, searchbyuni, UniSearchForm, CreateUserForm


# Create your views here.

def home(request):
    return render(request, 'website/home.html')


def resultpage(request):
    form = UniSearchForm(request.POST or None)

    if form.is_valid():
        results = []
        if form.cleaned_data['university']:
            faculties = Faculties.objects.filter(university=form.cleaned_data['university'])
            results.append(Department.objects.filter(faculty__in=faculties))

        if form.cleaned_data['total_year']:
            results.append(Department.objects.filter(total_year=form.cleaned_data['total_year']))
        if form.cleaned_data['scholarship']:
            results.append(Department.objects.filter(scholarship__in=form.cleaned_data['scholarship']))
        if form.cleaned_data['score'] is not None:
            results.append(Department.objects.filter(score__lte=form.cleaned_data['score']))
        if form.cleaned_data['edu_field']:
            for faculty in Faculties.objects.filter(edu_field=form.cleaned_data['edu_field']):
                results.append(Department.objects.filter(faculty=faculty))

        if form.cleaned_data['city']:
            for university in University.objects.filter(city__in=form.cleaned_data['city']):
                results.append(Department.objects.filter(faculty__in=Faculties.objects.filter(university=university)))
        if len(results) > 0:
            search_results = set(results[0])
            for result in results[1:]:
                search_results = search_results.intersection(result)
        else:
            search_results = Department.objects.all()

    context = {
        'data': search_results,
    }
    return render(request, 'website/resultpage.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('unilist')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('unilist')
            else:
                messages.info(request, 'Kullanıcı Adı veya Şifre hatalı.')
    return render(request, 'website/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.user.is_authenticated:
        return redirect('unilist')
    else:
        form = CreateUserForm();

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

                return redirect('login')

    return render(request, 'website/signup.html', {'form': form})


def unisozluk(request):
    return render(request, 'website/unisozluk.html')


def unipage(request):
    return render(request, 'website/unipage.html')


def uniedit(request):
    return render(request, 'website/uniedit.html')


@login_required(login_url='login')
def profile(request):
    return render(request, 'website/profile.html')


@login_required(login_url='login')
def unilist(request):
    return render(request, 'website/unilist.html')


@register.filter
def to_class_name(value):
    return value.__class__.__name__


def controlpanel(request):
    item = request.GET
    uni_form = searchbyuni(item or None)

    results = []

    scholarships = {
        -1: 'Ücretsiz',
        0: '%100 Burslu',
        1: '%75 Burslu',
        2: '%50 Burslu',
        3: '%25 Burslu'
    }
    if uni_form.is_valid():
        unis = University.objects.filter(name__contains=uni_form.cleaned_data['search_key'])
    else:
        unis = University.objects.all()

    for i, university in enumerate(unis):
        uni_obj = {}
        uni_obj['name'] = university.name
        uni_obj['type'] = 'university'
        uni_obj['id'] = f'{university.pk}-{university.name}'
        uni_obj['pk'] = university.pk
        results.append(uni_obj)
        faculties = Faculties.objects.filter(university=university)
        for faculty in faculties:
            faculty_obj = {}
            faculty_obj['name'] = faculty.name
            faculty_obj['parent_id'] = uni_obj['id']
            faculty_obj['id'] = f'{faculty.pk}-{faculty.name}'
            faculty_obj['pk'] = faculty.pk
            faculty_obj['type'] = 'faculty'
            results.append(faculty_obj)
            departmants = Department.objects.filter(faculty=faculty)
            for dep in departmants:
                dep_obj = {}
                dep_obj['name'] = f'{dep.name}-{scholarships[dep.scholarship]}'
                dep_obj['parent_id'] = faculty_obj['id']
                dep_obj['id'] = f'{dep.pk}-{dep.name}'
                dep_obj['pk'] = dep.pk
                dep_obj['type'] = 'departmant'
                results.append(dep_obj)

    context = {
        'data': results
    }
    return render(request, 'website/controlpanel.html', context)


def assistant(request):
    form = UniSearchForm(None)
    context = {
        'form': form
    }
    return render(request, 'website/assistant.html', context)


def userprofile(request):
    return render(request, 'website/userprofile.html')


@login_required(login_url='login')
def settings(request):
    return render(request, 'website/settings.html')


@login_required(login_url='login')
def settings2(request):
    return render(request, 'website/settings2.html')


@login_required
def add_uni(request):
    user = request.user
    admin = Admin.objects.filter(user=user)

    if len(admin) > 0 or True:
        form = UniForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print(form.cleaned_data)
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect('/admin/controlpanel')

    context = {
        "form": form
    }
    return render(request, 'website/adduni.html', context)


@login_required
def add_faculty(request):
    user = request.user
    admin = Admin.objects.filter(user=user)

    if len(admin) > 0 or True:
        faculty_form = FacultyForm(request.POST or None)
        if faculty_form.is_valid():
            faculty_form.save()
            return HttpResponseRedirect('/admin/controlpanel')

    context = {
        "faculty_form": faculty_form
    }
    return render(request, 'website/add_faculty.html', context)


@login_required
def edit_faculty(request, pk):
    detail = get_object_or_404(Faculties, pk=pk)
    form = FacultyForm(request.POST or None, instance=detail)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/admin/controlpanel')

    context = {
        "faculty_form": form,
        'edit': 'true',
        'pk': pk
    }
    return render(request, 'website/add_faculty.html', context)


@login_required
def edit_university(request, pk):
    detail = get_object_or_404(University, pk=pk)
    form = UniForm(request.POST or None, instance=detail)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/admin/controlpanel')

    context = {
        "form": form,
        'edit': 'true',
        'pk': pk
    }
    return render(request, 'website/adduni.html', context)


@login_required
def edit_departmant(request, pk):
    detail = get_object_or_404(Department, pk=pk)
    form = DepartForm(request.POST or None, instance=detail)

    if form.is_valid():
        uni = form.cleaned_data['faculty'].university
        if uni.types == 'public' and form.cleaned_data['scholarship'] != -1:
            form.add_error('scholarship', 'Devlet üniversitelerinde burs seçilemez!')
        elif uni.types == 'feepaying' and form.cleaned_data['scholarship'] == -1:
            form.add_error('scholarship', 'Özel üniversitelerinde ücretsiz seçilemez!')
        else:
            form.save()
            return HttpResponseRedirect('/admin/controlpanel')

    context = {
        "departmant_form": form,
        'edit': 'true',
        'pk': pk
    }
    return render(request, 'website/add_departmant.html', context)


@login_required
def add_departmant(request):
    user = request.user
    admin = Admin.objects.filter(user=user)

    if len(admin) > 0 or True:
        departmant_form = DepartForm(request.POST or None)
        if departmant_form.is_valid():
            uni = departmant_form.cleaned_data['faculty'].university
            if uni.types == 'public' and departmant_form.cleaned_data['scholarship'] != -1:
                departmant_form.add_error('scholarship', 'Devlet üniversitelerinde burs seçilemez!')
            elif uni.types == 'feepaying' and departmant_form.cleaned_data['scholarship'] == -1:
                departmant_form.add_error('scholarship', 'Özel üniversitelerinde ücretsiz seçilemez!')
            else:
                departmant_form.save()
                return HttpResponseRedirect('/admin/controlpanel')

    context = {
        "departmant_form": departmant_form
    }
    return render(request, 'website/add_departmant.html', context)


@login_required
def delete_uni(request, pk):
    query = get_object_or_404(University, pk=pk)
    query.delete()
    return HttpResponseRedirect('/admin/controlpanel')


@login_required
def delete_faculty(request, pk):
    query = get_object_or_404(Faculties, pk=pk)
    query.delete()
    return HttpResponseRedirect('/admin/controlpanel')


@login_required
def delete_departmant(request, pk):
    query = get_object_or_404(Department, pk=pk)
    query.delete()
    return HttpResponseRedirect('/admin/controlpanel')
