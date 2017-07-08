from django.contrib import admin
from django.contrib.auth.models import Permission
# Register your models here.

from .models import Area, Employee, Technical

admin.site.register(Area)
admin.site.register(Employee)
admin.site.register(Technical)
admin.site.register(Permission)
