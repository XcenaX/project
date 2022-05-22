from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('', views.IndexView.as_view(), name='index'), 
    path("tasks/<slug:id>", views.TaskView.as_view(), name="task"),     
    path('settings', views.SettingsView.as_view(), name='settings'),     
    path('reservations', views.ReservationsView.as_view(), name='reservations'),
    path('history', views.HistoryView.as_view(), name='history'),
    path('update_avatar', views.UpdateAvatar.as_view(), name='update_avatar'),
]