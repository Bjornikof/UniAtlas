from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import fields
from django.core.validators import MaxValueValidator, MinValueValidator

SCHOLARSHIP_CHOICES = [
    (-1, 'Ücretsiz'),
    (0, '%100 Burslu'),
    (1, '%75 Burslu'),
    (2, '%50 Burslu'),
    (3, '%25 Burslu')
]


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
        choices=STATUS_CHOICES,
        default=1
    )

    def __str__(self):
        return self.user.username


class University(models.Model):
    image = models.ImageField(upload_to='uni_image', null=True, blank=True, default='uni_image/default')
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    history = models.TextField(max_length=500)

    TYPE_CHOICES = [
        ("feepaying", 'Özel Okul'),
        ("public", 'Devlet Okulu'),

    ]

    types = models.CharField(
        choices=TYPE_CHOICES,
        default=None,
        max_length=100
    )

    def __str__(self):
        return self.name


class UniversityTag(models.Model):
    campus_info = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self


class Faculties(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    EDU_FIELD_CHOICES = [
        ("mf", 'Sayısal'),
        ("tm", 'Eşit Ağırlık'),
        ("söz", 'Sözel'),
        ("dil", 'Dil')
    ]

    edu_field = models.CharField(
        choices=EDU_FIELD_CHOICES,
        default=None,
        max_length=100,
    )

    def __str__(self):
        return f'{self.university.name}-{self.name}'

    class Meta:
        unique_together = (('university', 'name'),)


class Department(models.Model):
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    TOTAL_YEAR_CHOICES = [
        ("tdegree", 'İki Yıllık'),
        ("fdegree", 'Dört Yıllık'),
    ]

    total_year = models.CharField(
        choices=TOTAL_YEAR_CHOICES,
        max_length=100,
    )

    scholarship = models.IntegerField(choices=SCHOLARSHIP_CHOICES, default=-1)

    score = models.FloatField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('scholarship', 'name'),)


class Comment(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    enrolee = models.ForeignKey(Enrolee, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    text = models.TextField(max_length=500)
    date = models.DateTimeField()

    def __str__(self):
        return self.text


class Unitable(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    student = models.ForeignKey(Enrolee, on_delete=models.CASCADE)

    def __str__(self):
        return self
