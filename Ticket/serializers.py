from rest_framework.serializers import ModelSerializer
from Ticket.models import ServiceType, Ticket, Activity
from rest_framework.fields import SerializerMethodField, DateTimeField
from Service.models import Category
from Service.serializers import CategorySerializer, ServiceSerializer
from Enterprise.serializers import EmployeeSerializer, TechnicalSerializer
from rest_framework.settings import api_settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

class ServiceTypeSerializer(ModelSerializer):

    class Meta:
        model = ServiceType
        fields = '__all__'


class TicketSerializer(ModelSerializer):
    date = DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    status_time = SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'number', 'subject', 'description', 'date', 'status',
                  'solution', 'employee', 'service', 'service_type', 'was_attended',
                  'status_time']
        read_only_fields = ['id', 'number', 'date', 'status_time']

    def __init__(self, *args, **kwargs):
        super(TicketSerializer, self).__init__(*args, **kwargs)

        if self.context['request'].method == 'GET':
            self.fields['employee'] = EmployeeSerializer(read_only=True,
                                                         context=kwargs['context'])
            self.fields['was_attended'] = TechnicalSerializer(read_only=True,
                                                              context=kwargs['context'])
            self.fields['service_type'] = ServiceTypeSerializer(read_only=True,
                                                                context=kwargs['context'])
            self.fields['service'] = ServiceSerializer(read_only=True,
                                                       context=kwargs['context'])

    def get_status_time(self, obj):
        date_end = obj.date + timedelta(seconds=obj.service.ans * 60)
        date_format = datetime.strftime(obj.date, "%d-%m-%Y %H:%M:%S")
        date_end_format = datetime.strftime(date_end, "%d-%m-%Y %H:%M")

        if date_end > timezone.now():
            status_time = "timeleft"
            time = date_end - timezone.now()
            if (time.total_seconds() / 60) < 0.3 * obj.service.ans:
                if obj.status != 1 and obj.status != 2:
                    obj.status = 3
                    obj.save()
        else:
            status_time = "timeout"
            time = timezone.now() - date_end
            if obj.status != 1 and obj.status != 2:
                obj.status = 4
                obj.save()
                send_mail(
                    "Tiempo de ticket excedido",
                    "El técnico "+ obj.was_attended.employee.user.get_full_name() +
                    "Ha incumplido con dar solucion al ticket número " +
                    str(obj.number) +
                    "Pongase en contacto con el tecnico para dar solucion a esta" +
                    "situacion. Ingrese a http://localhost:8000",
                    settings.EMAIL_HOST_USER,
                    [obj.was_attended.boss.user.email],
                    fail_silently=False,
                )
        return {"time": time.total_seconds(), "date_end": date_end_format,
                "status_time": status_time, "date": date_format}
#     def to_representation(self, obj):
#         """Move fields from profile to user representation."""
#         rep = super().to_representation(obj)
#         if 'create' in self.context['request']:
#             rep.pop('number')
#         return rep


class ActivitySerializer(ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'
