from django.db import models
from distribution.yandex_s3_storage import ClientDocsStorage
import datetime
from django.contrib.auth.models import AbstractUser

from main.modules.hashutils import make_pw_hash

class Role(models.Model):
    name = models.TextField(default='')
    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.TextField(default='') 
    def __str__(self):
        return self.name


class User(AbstractUser):
    full_name = models.TextField(default='')
    work_experience = models.TextField(default='')
    telegram = models.TextField(default='')
    vk = models.TextField(default='')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True, default=Role.objects.filter(name="user").first().pk)    
    password = models.TextField(blank=True, null=True)
    image = models.FileField(storage=ClientDocsStorage(), blank=True, null=True)
    technologies = models.ManyToManyField(Technology)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_pw_hash(self.password)
        super(User, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.full_name


class Task(models.Model):
    name = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True, default=True)
    technologies = models.ManyToManyField(Technology)
    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True, default=True) 
    tasks = models.ManyToManyField(Task, null=True, blank=True)
    def __str__(self):
        return self.name