from django.conf.urls import url
from django.contrib import admin
from Service import views

app_name = 'Service'

urlpatterns = [
    url(r'^services/$',
        views.ServiceAPI.as_view({'get': 'list', 'post': 'create'}), name='service-list'),
    url(r'^services/(?P<id>[0-9]+)/$',
        views.ServiceAPI.as_view(
            {'get': 'retrieve', 'put': 'update', "patch": "partial_update"}
            ),
        name='service-detail'),
    url(r'^categorys/$',
        views.CategoryAPI.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    url(r'^categorys/(?P<id>[0-9]+)/$',
        views.CategoryAPI.as_view(
            {'get': 'retrieve', 'put': 'update', "patch": "partial_update"}
            ),
        name='category-detail'),
    url(r'^service-prioritys/$',
        views.ServicePriorityAPI.as_view({'get': 'list'}), name='service-priority-list'),
]
