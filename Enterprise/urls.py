from django.conf.urls import url
from Enterprise import views

app_name = 'Enterprise'

urlpatterns = [
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^$', views.Dashbboard.as_view(), name='dashboard'),
    url(r'^employees/$',
        views.EmployeeAPI.as_view({'get': 'list', 'post': 'create'}), name='employee-list'),
    url(r'^employees/(?P<id>[0-9]+)/$',
        views.EmployeeAPI.as_view(
            {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}
            ),
        name='employee-detail'),
    url(r'^technicals/$',   
        views.TechnicalAPI.as_view({'get': 'list', 'post': 'create'}), name='technical-list'),
    url(r'^technicals/(?P<id>[0-9]+)/$',
        views.TechnicalAPI.as_view({'get': 'retrieve', 'put': 'update'}), name='technical-detail'),
    url(r'^areas/$',
        views.AreaAPI.as_view({'get': 'list', 'post': 'create'}), name='area-list'),
    url(r'^areas/(?P<id>[0-9]+)/$',
        views.AreaAPI.as_view(
            {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}
            ),
        name='area-detail'),
    url(r'^autocomplete/$', views.autocomplete, name='autocomplete'),
]