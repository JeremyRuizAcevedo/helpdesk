from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import permission_classes, authentication_classes,\
    renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.generic import View
from rest_framework.authentication import SessionAuthentication,\
    BasicAuthentication
from rest_framework.viewsets import ModelViewSet
from Enterprise.serializers import EmployeeSerializer, TechnicalSerializer,\
    AreaSerializer, UserSerializer
from Enterprise.models import Employee, Technical, Area
from rest_framework.urls import template_name
from django.http.response import JsonResponse
from Ticket.models import Ticket
from django.db.models.aggregates import Count
from django.contrib.auth.models import User
# Create your views here.

class Login(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Enterprise/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("Enterprise:dashboard")
        return Response({})

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return redirect("Enterprise:login")
        return redirect("Enterprise:dashboard")


class Register(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Enterprise/registration.html'

    def get(self, request, *args, **kwargs):
        return Response({})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print('Usuario ya registrado')
        else:
            print('registrar')
        return render(request, self.template, self.get_context())


class Dashbboard(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Enterprise/dashboard.html'

    def get(self, request, *args, **kwargs):
        if request.user.get_all_permissions() == {'auth.is_employee'}:
            return redirect("Ticket:ticket-list")
        return Response({}, template_name = 'Enterprise/dashboard.html')


class Logout(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('Enterprise:login')


class AreaAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AreaSerializer
    queryset = Area.objects.filter(n_status=True)
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        response = super(AreaAPI, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'create' in request.query_params:
                return Response({}, template_name = 'Enterprise/create-area.html')
            else:
                return Response({'areas': response.data},
                                template_name = 'Enterprise/list-areas.html')
        return response
    
    def create(self, request, *args, **kwargs):
        response = super(AreaAPI, self).create(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return redirect('Enterprise:area-list')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(AreaAPI, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'name' not in request.GET:
                return Response({'area': response.data},
                            template_name = 'Enterprise/edit-area.html')
            else:
                return redirect('Enterprise:area-list')
        return response

class EmployeeAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.filter(n_status=True)
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    lookup_field = 'id'
    
    def list(self, request, *args, **kwargs):
        response = super(EmployeeAPI, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'create' in request.query_params:
                areas = Area.objects.all()
                area = AreaSerializer(areas, many=True, context={'request': request})
                return Response({'areas': area.data},
                                template_name = 'Enterprise/create-employee.html')
            else:
                return Response({'employees': response.data},
                                template_name = 'Enterprise/list-employees.html')
        return response

    def create(self, request, *args, **kwargs):
        response = super(EmployeeAPI, self).create(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return redirect('Enterprise:employee-list')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(EmployeeAPI, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'employee': response.data},
                            template_name = 'Enterprise/edit-employee.html')
        return response


class TechnicalAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]  
    serializer_class = TechnicalSerializer
    queryset = Technical.objects.filter(employee__n_status=True)
    renderer_classes = [JSONRenderer]
    lookup_field = 'id'
    
    def get_queryset(self):
        if 'free_technical' in self.request.query_params:
            busy_technicals = list(Ticket.objects.\
                                   values_list("was_attended", flat=True).distinct())
            id_service = self.request.query_params["service"]
            free_technical = Technical.objects.\
                                filter(employee__n_status=True, services__id=id_service).\
                                exclude(id__in=busy_technicals)
            queryset = free_technical
        else:
            queryset = Technical.objects.filter(employee__n_status=True)
        return queryset


def autocomplete(request):
    if request.is_ajax():
        queryset = Employee.objects.filter(user__username__startswith=request.GET.get('search', None))
        list = []        
        for i in queryset:
            list.append(i.user.username)
        data = {
            'list': list,
        }
        return JsonResponse(data)
    return render(request, "Enterprise/autocomplete.html", {})
