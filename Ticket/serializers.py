from rest_framework.serializers import ModelSerializer
from Ticket.models import ServiceType, Ticket, Activity
from rest_framework.fields import SerializerMethodField, DateTimeField
from Service.models import Category
from Service.serializers import CategorySerializer
from Enterprise.serializers import EmployeeSerializer, TechnicalSerializer
from rest_framework.settings import api_settings

class ServiceTypeSerializer(ModelSerializer):
    
    class Meta:
        model = ServiceType
        fields = '__all__'


class TicketSerializer(ModelSerializer):
    service_type = ServiceTypeSerializer(read_only=True)
    date = DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = Ticket
        fields = ['id', 'number', 'subject', 'description', 'date', 'status',
                  'solution', 'employee', 'service', 'service_type', 'was_attended']
        read_only_fields = ['id'', number', 'date', 'employee']

    def __init__(self, *args, **kwargs):
        super(TicketSerializer, self).__init__(*args, **kwargs)

        if self.context['request'].method == 'GET':
            self.fields['employee'] = EmployeeSerializer(read_only=True,
                                                         context=kwargs['context'])
            self.fields['was_attended'] = TechnicalSerializer(read_only=True,
                                                              context=kwargs['context'])

#     def to_representation(self, obj):
#         """Move fields from profile to user representation."""
#         rep = super().to_representation(obj)
#         if 'create' in self.context['request']:
#             rep.pop('number')
#         return rep


class ActivitySerializer(ModelSerializer):

    class Meta:
        model = Activity
        fields= '__all__'