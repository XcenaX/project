from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('', views.IndexView.as_view(), name='index'), 
    path("tasks/<slug:id>", views.TaskView.as_view(), name="task"),    
]