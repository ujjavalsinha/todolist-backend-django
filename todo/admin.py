from django.contrib import admin
from .models import Todo, Bucket
# Register your models here.

admin.site.register(Todo)
admin.site.register(Bucket)