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
from Enterprise.models import Technical, Employee
from Enterprise.serializers import TechnicalSerializer
from Service.models import Category
from Service.serializers import CategorySerializer
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


class TicketAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'Ticket/list-tickets.html'
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        response = super(TicketAPI, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'create' in request.query_params:
                services_types = ServiceType.objects.all()
                services_type = ServiceTypeSerializer(
                    services_types, many=True)
                categorys = Category.objects.all()
                category = CategorySerializer(
                    categorys, many=True, context={'request': request})
                return Response({'service_types': services_type.data,
                                 'categorys': category.data},
                                template_name='Ticket/create-ticket.html')
            else:
                return Response({'tickets': response.data},
                                template_name='Ticket/list-tickets.html')
        return response

    def get_queryset(self):
        if self.request.user.is_authenticated() and not self.request.user.has_perm("auth.is_admin"):
            queryset = Ticket.objects.filter(
                employee=self.request.user.employee)
        else:
            queryset = Ticket.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        response = super(TicketAPI, self).create(request, *args, **kwargs)
        print(request.data)
        id_employee = request.data["employee"]
        id_technical = request.data["was_attended"]
        employee = Employee.objects.filter(id=id_employee).last()
        ticket = Ticket.objects.filter(
            employee=employee).order_by('date').last()
        technical = Technical.objects.filter(id=id_technical).last()
        send_mail(
            "Nueva ticket registrado",
            "Usted ha registrado un ticket con éxito. El número de su ticket es: " +
            str(ticket.number) +
            "Le atenderemos en la brevedad posible. Ingrese a http://localhost:8000",
            settings.EMAIL_HOST_USER,
            [employee.user.email],
            fail_silently=False,
        )
        send_mail(
            "Nuevo ticket registrado",
            "Usted tiene un nuevo ticket a resolver. Ingrese a http://localhost:8000",
            settings.EMAIL_HOST_USER,
            [technical.employee.user.email],
            fail_silently=False,
        )
        if request.accepted_renderer.format == 'html':
            return redirect('Ticket:ticket-list')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(TicketAPI, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'name' not in request.GET:
                return Response({'ticket': response.data},
                                template_name='Ticket/edit-ticket.html')
            else:
                return redirect('Ticket:ticket-list')
        return response
