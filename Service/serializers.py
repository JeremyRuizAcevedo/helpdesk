from rest_framework.serializers import ModelSerializer
from Service.models import Service, Category, ServicePriority

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'



class ServicePrioritySerializer(ModelSerializer):

    class Meta:
        model = ServicePriority
        fields = ['name']


class ServiceSerializer(ModelSerializer):
#     category = CategorySerializer()
#     priority = ServicePrioritySerializer()
    class Meta:
        model = Service
        fields = ['id', 'name', 'priority', 'ans', 'notification',
                  'notification_boss', 'category']
        read_only_fields = ['id', 'notification', 'notification_boss']
        
    def create(self, validated_data):
        print(validated_data)