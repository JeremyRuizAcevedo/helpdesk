from django.contrib import admin

# Register your models here.

from .models import Question, Alternative, Poll

admin.site.register(Question)
admin.site.register(Alternative)
admin.site.register(Poll)