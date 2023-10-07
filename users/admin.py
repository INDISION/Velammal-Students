from django.contrib import admin
from . import models

admin.site.register(models.StudentProfile)
admin.site.register(models.Department)
admin.site.register(models.Batch)
admin.site.register(models.Regulation)
admin.site.register(models.Year)
admin.site.register(models.Semester)
admin.site.register(models.Section)