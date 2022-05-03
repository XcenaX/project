from django.db import models
from distribution.yandex_s3_storage import ClientDocsStorage
import datetime
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.TextField(default='') 
    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.TextField(default='') 
    def __str__(self):
        return self.name


class User(AbstractUser):
    full_name = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    login = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    avatar = models.FileField(storage=ClientDocsStorage())


class Task(models.Model):
    name = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True, default=True)
    technologies = models.ManyToManyField(Technology)

class Project(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True, default=True) 
    tasks = models.ManyToManyField(Task, null=True, blank=True)
    def __str__(self):
        return self.name