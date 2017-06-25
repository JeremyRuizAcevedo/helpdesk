from rest_framework.serializers import ModelSerializer
from Ticket.models import ServiceType, Ticket, Activity
from rest_framework.fields import SerializerMethodField, DateTimeField
from Service.models import Category
from Service.serializers import CategorySerializer
from Enterprise.serializers import EmployeeSerializer
from rest_framework.settings import api_settings

class ServiceTypeSerializer(ModelSerializer):
    
    class Meta:
        model = ServiceType
        fields = '__all__'


class TicketSerializer(ModelSerializer):
#     categorys = SerializerMethodField()
#     service_types = SerializerMethodField()
    service_type = ServiceTypeSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    date = DateTimeField(format="%d-%m-%Y %H:%M")
    class Meta:
        model = Ticket
        fields = ['id', 'number', 'subject', 'description', 'date', 'status',
                  'solution', 'employee', 'service', 'service_type']
        read_only_fields = ['id'', number', 'date', 'employee']

    
#     def to_representation(self, obj):
#         """Move fields from profile to user representation."""
#         rep = super().to_representation(obj)
#         if 'create' in self.context['request']:
#             rep.pop('number')
#         return rep

#     def get_categorys(self, obj):
#         categorys = Category.objects.all()
#         serializer = CategorySerializer(categorys, many=True)
#         return serializer.data
# 
#     def get_service_types(self, obj):
#         service_types = ServiceType.objects.all()
#         serializer = ServiceTypeSerializer(service_types, many=True)
#         return serializer.data


class ActivitySerializer(ModelSerializer):

    class Meta:
        model = Activity
        fields= '__all__'