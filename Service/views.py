from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication,\
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from Service.models import Service, Category, ServicePriority
from Service.serializers import ServiceSerializer, CategorySerializer,\
    ServicePrioritySerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from Enterprise.views import MyHTMLRenderer

# Create your views here.
class ServiceAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    renderer_classes = [MyHTMLRenderer]
    template_name = 'Service/create-service.html'
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        categorys = Category.objects.all()
        category = CategorySerializer(categorys, many=True)
        prioritys = ServicePriority.objects.all()
        priority = ServicePrioritySerializer(prioritys, many=True)
        return Response({'categorys': category.data, 'prioritys': priority.data})
