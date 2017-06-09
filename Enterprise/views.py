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
    AreaSerializer
from Enterprise.models import Employee, Technical, Area
# Create your views here.

class MyHTMLRenderer(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        context = {'data': data}
        response = renderer_context['response']
        if response.exception:
            data['status_code'] = response.status_code
        return context


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
            if user.username == 'jeremy':
                login( request, user)
        else:
            self.message = "Username o password incorrectos"
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
        return render(request, self.template, self.get_context() )

class Dashbboard(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Enterprise/dashboard.html'

    def get(self, request, *args, **kwargs):
        return Response({})


class Logout(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('Enterprise:login')


class AreaAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    lookup_field = 'id'


class EmployeeAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = 'id'


class TechnicalAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TechnicalSerializer
    queryset = Technical.objects.all()
    lookup_field = 'id'
