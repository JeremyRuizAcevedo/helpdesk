""" Service Model """
from django.db import models

# Create your models here.


class Category(models.Model):
    """ Category model """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    n_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ServicePriority(models.Model):
    name = models.CharField(max_length=15, default='Baja')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50)
    priority = models.ForeignKey(ServicePriority)
    ans = models.IntegerField()
    notification = models.BooleanField(default=False)
    notification_boss = models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    n_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    service = models.ForeignKey(Service)

    def __str__(self):
        return self.name
