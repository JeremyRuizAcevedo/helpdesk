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
from rest_framework.urls import template_name
# Create your views here.


class MyHTMLRenderer(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):

        """
        Override of TemplateHTMLRenderer class method to display
        extra context in the template, which is otherwise omitted.
        """
        temp = data
        context = {'data': data}
        response = renderer_context['response']
        if response.exception:
            context = {'data':data}
            data['status_code'] = response.status_code
            return context
        else:
            print('aqui')
            context = temp
    
            # pop keys which we do not need in the template
            keys_to_delete = ['request', 'response', 'args', 'kwargs']
            for item in keys_to_delete:
                renderer_context.pop(item)
    
            for key, value in renderer_context.items():
                if key not in context:
                    context[key] = value
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
                login(request, user)
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
        return render(request, self.template, self.get_context())


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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Enterprise/list-areas.html'
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        response = super(AreaAPI, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'create' in request.query_params:
                return Response({}, template_name = 'Enterprise/create-area.html')
            else:
                return render({'areas': response.data},
                                template_name = 'Enterprise/list-areas.html')
        return response
    
    def retrieve(self, request, *args, **kwargs):
        response = super(AreaAPI, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'area': response.data},
                            template_name = 'Service/edit-area.html')
        return response

class EmployeeAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Enterprise/list-employees.html'
    lookup_field = 'id'
    
    def list(self, request, *args, **kwargs):
        response = super(EmployeeAPI, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            if 'create' in request.query_params:
                areas = Area.objects.all()
                area = AreaSerializer(areas, many=True)
                return Response({'areas': area.data},
                                template_name = 'Enterprise/create-employee.html')
            else:
                return render({'employees': response.data},
                                template_name = 'Enterprise/list-employees.html')
        return response
    
    def retrieve(self, request, *args, **kwargs):
        response = super(EmployeeAPI, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'employee': response.data},
                            template_name = 'Service/edit-employee.html')
        return response


class TechnicalAPI(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TechnicalSerializer
    queryset = Technical.objects.all()
    lookup_field = 'id'
