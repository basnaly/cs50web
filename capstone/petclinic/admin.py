from django.contrib import admin

from .models import User, Pet, Insurance, Visit

# Register your models here.

admin.site.register(User)
admin.site.register(Pet)
admin.site.register(Insurance)
admin.site.register(Visit)