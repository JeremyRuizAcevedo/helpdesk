from rest_framework.serializers import ModelSerializer
from Ticket.models import ServiceType, Ticket, Activity

class ServiceTypeSerializer(ModelSerializer):
    
    class Meta:
        model = ServiceType
        fields = '__all__'


class TicketSerializer(ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'


class ActivitySerializer(ModelSerializer):

    class Meta:
        model = Activity
        fields= '__all__'