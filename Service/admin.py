from django.contrib import admin
from .models import Category, Service, FAQ

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(FAQ)