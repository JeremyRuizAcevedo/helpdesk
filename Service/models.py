from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class ServicePriority(models.Model):
    name = models.CharField(max_length=15, default='Baja')
    description = models.TextField(blank=True, null=True)


class Service(models.Model):
    name = models.CharField(max_length=50)
    prioridad = models.ForeignKey(ServicePriority)
    ans = models.IntegerField()
    notification = models.BooleanField()
    notification_boss = models.BooleanField()
    category = models.ForeignKey(Category)
    
    def __str__(self):
        return self.name


class FAQ(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    service = models.ForeignKey(Service)
    
    def __str__(self):
        return self.name