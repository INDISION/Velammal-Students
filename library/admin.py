from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AuthorAndOrganization)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookId)
