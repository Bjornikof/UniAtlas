from django.contrib import admin

# Register your models here.
from website.models import Enrolee, Admin, University, Faculties, Department, Comment

admin.site.register(Enrolee)
admin.site.register(Admin)
admin.site.register(University)
admin.site.register(Faculties)
admin.site.register(Department)
admin.site.register(Comment)

