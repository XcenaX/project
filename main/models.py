from django.db import models
from distribution.yandex_s3_storage import ClientDocsStorage
import datetime
from django.contrib.auth.models import AbstractUser

from main.modules.hashutils import make_pw_hash

TASK_STATUS = (
    ("0", 'В процессе'),
    ("1", 'На проверке'),
    ("2", 'Возвращено'),
    ("3", 'Сделано'),    
)

def get_status_list():
    statuses = []
    for status in TASK_STATUS:
        statuses.append(status[1])
    return statuses

class Role(models.Model):
    name = models.TextField(default='')
    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.TextField(default='') 
    def __str__(self):
        return self.name


class User(AbstractUser):
    full_name = models.TextField(default='', blank=True)
    work_experience = models.TextField(default='', blank=True)
    telegram = models.TextField(default='', blank=True)
    vk = models.TextField(default='', blank=True)
    phone = models.TextField(default='', blank=True)
    email = models.TextField(default='', blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)    
    password = models.TextField(blank=True, null=True)
    image = models.FileField(storage=ClientDocsStorage(), blank=True, null=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_pw_hash(self.password)
        super(User, self).save(*args, **kwargs)
    @property
    def made_tasks(self):
        return len(Task.objects.filter(user=self, status="3"))
    def __str__(self):
        return self.full_name


class Task(models.Model):
    name = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    technologies = models.ManyToManyField(Technology)    
    status = models.CharField(max_length=1, choices=TASK_STATUS, default="0")

    def get_status_name(self):        
        return dict(TASK_STATUS)[self.status]        

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True, null=True) 
    tasks = models.ManyToManyField(Task, null=True, blank=True)
    workers = models.ManyToManyField(User, null=True, blank=True)
    def __str__(self):
        return self.name