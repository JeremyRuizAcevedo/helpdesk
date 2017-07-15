from django.conf.urls import url
from django.contrib import admin
from Ticket import views

app_name = 'Ticket'

urlpatterns = [
    url(r'^tickets/$',
        views.TicketAPI.as_view({'get': 'list', 'post': 'create'}), name='ticket-list'),
    url(r'^tickets/(?P<id>[0-9]+)/$',
        views.TicketAPI.as_view(
            {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}
        ),
        name='ticket-detail'),
]
