from rest_framework.serializers import ModelSerializer
from Enterprise.models import Employee, Technical, Area
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class AreaSerializer(ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


class TechnicalSerializer(ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = Technical
        fields = '__all__'