from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import authentication_classes,\
    permission_classes, renderer_classes
from rest_framework.authentication import SessionAuthentication,\
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from Ticket.models import Ticket, ServiceType
from Ticket.serializers import TicketSerializer, ServiceTypeSerializer
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.urls import template_name
from rest_framework.response import Response
from Enterprise.models import Technical
from Enterprise.serializers import TechnicalSerializer
from Service.models import Category
from Service.serializers import CategorySerializer

# Create your views here.
class TicketAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'Ticket/list-tickets.html'
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        response = super(TicketAPI, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'create' in request.query_params:
                services_types = ServiceType.objects.all()
                services_type = ServiceTypeSerializer(services_types, many=True)
                categorys = Category.objects.all()
                category = CategorySerializer(categorys, many=True, context={'request': request})
                return Response({'service_types': services_type.data,
                                 'categorys': category.data},
                                template_name = 'Ticket/create-ticket.html')
            else:
                return Response({'tickets': response.data},
                                template_name = 'Ticket/list-tickets.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(TicketAPI, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'name' not in request.GET:
                return Response({'ticket': response.data},
                            template_name = 'Ticket/edit-ticket.html')
            else:
                return redirect('Ticket:ticket-list')
        return response
