from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(Exam)
admin.site.register(Result)