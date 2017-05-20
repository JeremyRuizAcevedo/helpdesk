from django.db import models
from Enterprise.models import Employee

# Create your models here.
class Question(models.Model):
    statement = models.CharField(max_length=50)


class Alternative(models.Model):
    description = models.CharField(max_length=50)
    question = models.ForeignKey(Question)


class Poll(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    alternative = models.ForeignKey(Alternative)
    employee = models.ForeignKey(Employee)
