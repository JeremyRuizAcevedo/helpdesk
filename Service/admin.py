from django.contrib import admin
from .models import Category, Service, FAQ, ServicePriority

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(FAQ)
admin.site.register(ServicePriority)