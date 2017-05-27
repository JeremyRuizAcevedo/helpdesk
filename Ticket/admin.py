from django.contrib import admin

from .models import ServiceType, Ticket, Activity

admin.site.register(ServiceType)
admin.site.register(Ticket)
admin.site.register(Activity)