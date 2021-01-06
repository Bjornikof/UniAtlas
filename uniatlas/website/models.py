from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Enrolee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        (0, 'Liseli'),
        (1, 'Üniversiteli'),
        (2, 'Mezun'),

    ]

    status = models.IntegerField(
        choices= STATUS_CHOICES,
        default= 1
    )

    def __str__(self):
        return self.user.username



class University(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    history = models.TextField(max_length=500)

    TYPE_CHOICES = [
     ("feepaying", 'Özel Okul'),
     ("public", 'Devlet Okulu'),

    ]

    def __str__(self):
        return self.name


class UniversityTag(models.Model):
    campus_info = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self


class Faculties(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=100)


    EDU_FIELD_CHOICES = [
        ("mf", 'Sayısal'),
        ("tm", 'Eşit Ağırlık'),
        ("söz", 'Sözel'),
        ("dil", 'Dil'),
    ]

    edu_field = models.CharField(
        choices=EDU_FIELD_CHOICES,
        default=None,
        max_length=100,
    )

    def __str__(self):
        return self.faculty_name


class Department (models.Model):
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    TOTAL_YEAR_CHOICES = [
    ("tdegree", 'İki Yıllık'),
    ("fdegree", 'Dört Yıllık'),
    ]

    total_year = models.CharField(
    choices=TOTAL_YEAR_CHOICES,
    max_length= 100,
    )

    SCHOLARSHIP_CHOICES = [
      (0, '%100 Burslu'),
      (1, '%50 Burslu'),
      (2, '%25 Burslu'),
    ]

    scholarship = models.IntegerField(
        choices=SCHOLARSHIP_CHOICES,
        default=3,
        null=True,
        unique=True,
    )

    def __str__(self):
        return self.name

class Comment(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    enrolee = models.ForeignKey(Enrolee, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    text = models.TextField(max_length=500)
    date = models.DateTimeField()

    def __str__(self):
        return self.text

