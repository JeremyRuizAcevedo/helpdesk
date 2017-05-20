from django.contrib import admin

from .models import ServiceType, Ticket, Action

admin.site.register(ServiceType)
admin.site.register(Ticket)
admin.site.register(Action)