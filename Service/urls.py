from django.conf.urls import url
from django.contrib import admin
from Service import views

app_name = 'Service'

urlpatterns = [
    url(r'^services/',
        views.ServiceAPI.as_view({'get': 'list', 'post': 'create'}), name='list-service'),
]
