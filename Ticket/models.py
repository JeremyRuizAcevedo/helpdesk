from django.db import models
from Enterprise.models import Employee

# Create your models here.
class ServiceType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Ticket(models.Model):
    number = models.IntegerField()
    subject = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    solution = models.TextField()
    employee = models.ForeignKey(Employee)
    service_type = models.ForeignKey(ServiceType)
    
    def __str__(self):
        return self.number + self.subject


class Action(models.Model):
    date = models.DateTimeField(auto_now=True)
    description = models.TextField()
    ticket = models.ForeignKey(Ticket)
    is_solution = models.BooleanField(defautl=False)
    
    def __str__(self):
        return self.description
