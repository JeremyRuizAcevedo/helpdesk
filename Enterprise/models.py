from django.db import models
from Service.models import Service
from django.contrib.auth.models import User
from random import randrange

# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    n_status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    code = models.IntegerField(default=randrange(13200000, 13201999, 43))
    dni = models.IntegerField()
    phone = models.IntegerField(blank=True, null=True)
    area = models.ForeignKey(Area)
    n_status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.get_full_name()


class Technical(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    boss = models.ForeignKey(Employee, related_name="boss")
    status = models.BooleanField()
    services = models.ManyToManyField(Service)
    
    def __str__(self):
        return self.employee.user.get_full_name()
