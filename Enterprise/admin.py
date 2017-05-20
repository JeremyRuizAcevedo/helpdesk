from django.contrib import admin

# Register your models here.

from .models import Area, Employee, Technical

admin.site.register(Area)
admin.site.register(Employee)
admin.site.register(Technical)
