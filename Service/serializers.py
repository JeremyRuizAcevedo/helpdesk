from rest_framework.serializers import ModelSerializer
from Service.models import Service, Category, ServicePriority
from rest_framework.relations import StringRelatedField, PrimaryKeyRelatedField
from rest_framework.fields import SerializerMethodField
from rest_framework.renderers import JSONRenderer


class CategorySerializer(ModelSerializer):
    services = SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'services']
        read_only_fields = ['id']
    
#     def to_representation(self, obj):
#         """Move fields from profile to user representation."""
#         rep = super().to_representation(obj)
#         print(self.context['request'])
#         if 'detail' in self.context['request']:
#             rep.pop('services')
#         return rep
# # 
    def get_services(self,obj):
        services = Service.objects.filter(category=obj)
        list_services = []
        dict_service = {}
        for service in services:
            dict_service = {'id': service.id, 'name': service.name}
            list_services.append(dict_service)
        return list_services
            

class ServicePrioritySerializer(ModelSerializer):

    class Meta:
        model = ServicePriority
        fields = '__all__'


class ServiceSerializer(ModelSerializer):
    category = CategorySerializer()
    priority = ServicePrioritySerializer()
    class Meta:
        model = Service
        fields = ['id', 'name', 'priority', 'ans', 'notification',
                  'notification_boss', 'category']
        read_only_fields = ['id', 'notification', 'notification_boss']
