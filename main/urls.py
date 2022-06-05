from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('', views.IndexView.as_view(), name='index'),     
    path("tasks/<slug:id>", views.TaskView.as_view(), name="task"),     
    path('set_task_status/<slug:id>', views.SetTaskStatus.as_view(), name='set_task_status'),
    path('settings', views.SettingsView.as_view(), name='settings'),     
    path('projects', views.ProjectsView.as_view(), name='projects'),
    path('add_project', views.AddProjectView.as_view(), name='add_project'),
    path('delete_project/<slug:id>', views.DeleteProjectView.as_view(), name='delete_project'),
    path('history', views.HistoryView.as_view(), name='history'),
    path('manager_tasks', views.TasksView.as_view(), name='manager_tasks'),
    path('workers', views.WorkersView.as_view(), name='workers'),
    path('add_worker', views.AddWorkerView.as_view(), name='add_worker'),
    path('delete_worker/<slug:id>', views.DeleteWorkersView.as_view(), name='delete_worker'),
    path('update_avatar', views.UpdateAvatar.as_view(), name='update_avatar'),
    path('table_data', views.TableDataView.as_view(), name='table_data'),
]