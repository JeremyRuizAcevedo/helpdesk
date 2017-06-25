from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication,\
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from Service.models import Service, Category, ServicePriority
from Service.serializers import ServiceSerializer, CategorySerializer,\
    ServicePrioritySerializer
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

# Create your views here.


class CategoryAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        response = super(CategoryAPI, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'create' in request.query_params:
                return Response({}, template_name = 'Service/create-category.html')
            else:
                return Response({'data': response.data},
                                template_name = 'Service/list-categorys.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(CategoryAPI, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'name' not in request.GET:
                return Response({'category': response.data},
                                template_name = 'Service/edit-category.html')
            else:
                return redirect('Service:category-list')
        return response


class ServiceAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    renderer_classes = [TemplateHTMLRenderer]
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
            response = super(ServiceAPI, self).list(request, *args, **kwargs)
            return Response({'data': response.data},
                                template_name = 'Service/list-services.html')
