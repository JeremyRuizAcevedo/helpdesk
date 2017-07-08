from rest_framework.serializers import ModelSerializer
from Service.models import Service, Category, ServicePriority
from rest_framework.relations import StringRelatedField, PrimaryKeyRelatedField
from rest_framework.fields import SerializerMethodField
from rest_framework.renderers import JSONRenderer


class CategorySerializer(ModelSerializer):
    services = SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'n_status','services']
        read_only_fields = ['id']
    
    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        rep = super().to_representation(obj)
        if 'category_services' not in self.context['request'].GET:
            rep.pop('services')
        return rep
# # 
    def get_services(self,obj):
        if "category_services" in self.context["request"].GET:
            services = Service.objects.filter(category=obj)
            list_services = []
            dict_service = {}
            for service in services:
                dict_service = {'id': service.id, 'name': service.name}
                list_services.append(dict_service)
            return list_services

    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)

        if self.context['request'].method == 'GET' or self.context['request'].method == 'POST':
            self.fields.pop("n_status")


class ServicePrioritySerializer(ModelSerializer):

    class Meta:
        model = ServicePriority
        fields = '__all__'


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'priority', 'ans', 'notification',
                  'notification_boss', 'category', 'n_status']
        read_only_fields = ['id', 'notification', 'notification_boss']
    
    def __init__(self, *args, **kwargs):
        super(ServiceSerializer, self).__init__(*args, **kwargs)
 
        if self.context['request'].method == 'GET':
            self.fields['category'] = CategorySerializer(read_only=True, context=kwargs['context'])
            self.fields['priority'] = ServicePrioritySerializer(read_only=True, context=kwargs['context'])

        if self.context['request'].method == 'GET' or self.context['request'].method == 'POST':
            self.fields.pop("n_status")
