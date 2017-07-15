""" Serializers of Ticket """
from Enterprise.models import Employee, Technical, Area
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from Service.serializers import ServiceSerializer


class UserSerializer(ModelSerializer):
    name = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'first_name', 'last_name', 'email', 'name']
        write_only_fields = ['password']

    def get_name(self, obj):
        return obj.get_full_name()


class AreaSerializer(ModelSerializer):

    class Meta:
        model = Area
        fields = ['id', 'name', 'description', "n_status"]
        read_only_fields = ['id']
#

    def __init__(self, *args, **kwargs):
        super(AreaSerializer, self).__init__(*args, **kwargs)

        if self.context['request'].method == 'GET' or self.context['request'].method == 'POST':
            self.fields.pop("n_status")


class EmployeeSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployeeSerializer, self).__init__(*args, **kwargs)

        if self.context['request'].method == 'GET':
            self.fields['area'] = AreaSerializer(
                read_only=True, context=kwargs['context'])

        if self.context['request'].method == 'GET' or self.context['request'].method == 'POST':
            self.fields.pop("n_status")

    def create(self, validated_data):
        username = validated_data["user"]["username"]
        first_name = validated_data["user"]["first_name"]
        last_name = validated_data["user"]["last_name"]
        email = validated_data["user"]["email"]
        password = validated_data["user"]["password"]
        dni = validated_data["dni"]
        phone = validated_data["phone"]
        area = validated_data["area"]
        user = User.objects.create(username=username, first_name=first_name,
                                   last_name=last_name, email=email)
        user.set_password(password)
        user.save()
        employee = Employee.objects.create(
            user=user, dni=dni, phone=phone, area=area)
        send_mail(
            "Nueva cuenta de empleado",
            "Usted ha sido registrado con exito y forma parte del sistema\
                de mesa de ayuda. Esta es su contraseña: " + password + ". Se le \
                sugiere cambiarla e iniciar sesion",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return employee


class TechnicalSerializer(ModelSerializer):
    class Meta:
        model = Technical
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TechnicalSerializer, self).__init__(*args, **kwargs)

        if self.context['request'].method == 'GET':
            self.fields['employee'] = EmployeeSerializer(
                read_only=True, context=kwargs['context'])
            self.fields['services'] = ServiceSerializer(read_only=True, many=True,
                                                        context=kwargs['context'])
