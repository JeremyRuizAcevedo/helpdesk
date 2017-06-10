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


class CategoryAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [MyHTMLRenderer]
    template_name = 'Service/list-categorys.html'
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        if 'create' in request.query_params:
            return Response({}, template_name = 'Service/create-category.html')
        else:
            return ModelViewSet.list(self, request, *args, **kwargs)


class ServiceAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    renderer_classes = [MyHTMLRenderer]
    template_name = 'Service/list-services.html'
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        if 'create' in request.query_params:
            categorys = Category.objects.all()
            category = CategorySerializer(categorys, many=True)
            prioritys = ServicePriority.objects.all()
            priority = ServicePrioritySerializer(prioritys, many=True)
            return Response({'categorys': category.data, 'prioritys': priority.data},
                            template_name = 'Service/create-service.html')
        else:
            return ModelViewSet.list(self, request, *args, **kwargs)
