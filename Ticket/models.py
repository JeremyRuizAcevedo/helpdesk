from django.db import models
from Enterprise.models import Employee, Technical
from random import randrange
from Service.models import Service
from django.utils import timezone

# Create your models here.


class ServiceType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    number = models.IntegerField(default=randrange(100, 999, 7))
    subject = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)
    solution = models.TextField(default="")
    employee = models.ForeignKey(Employee, null=True, blank=True)
    service = models.ForeignKey(Service, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType)
    was_attended = models.ForeignKey(Technical, null=True, blank=True)

    def __str__(self):
        return str(self.number) + " - " + self.subject


class Activity(models.Model):
    date = models.DateTimeField(auto_now=True)
    description = models.TextField()
    ticket = models.ForeignKey(Ticket, null=True, blank=True)
    is_solution = models.BooleanField(default=False)

    def __str__(self):
        return self.description
