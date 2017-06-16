from django.conf.urls import url
from django.contrib import admin
from Enterprise import views

app_name = 'Enterprise'

urlpatterns = [
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^employee-api/$', views.EmployeeAPI.as_view({'get': 'list', 'post': 'create'})),
    url(r'^technical-api/$', views.TechnicalAPI.as_view({'get': 'list', 'post': 'create'})),
    url(r'^dashboard/$', views.Dashbboard.as_view(), name='dashboard'),
]