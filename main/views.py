from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.dispatch import receiver
from django.db.models.signals import *

from main.modules.hashutils import check_pw_hash, make_pw_hash

from .modules.functions import *

from main.models import *

class LoginView(View):
    template_name = "login.html"
    def get(self, request, *args, **kwargs):                            
        return render(request, self.template_name, {})
    def post(self, request, *args, **kwargs):
        login = post_parameter(request, "login")
        password = post_parameter(request, "password")        
        user = None
        try:
            user = User.objects.get(username=login)
        except:
            return render(request, self.template_name, {
                "error": "Неверный логин или пароль!"
            })
        if check_pw_hash(password, user.password):
            request.session["user"] = user.id
            return redirect(reverse("main:index"))
        return render(request, self.template_name, {
            "error": "Неверный логин или пароль!"
        })

class RegisterView(View):
    template_name = "register.html"
    def get(self, request, *args, **kwargs):                            
        return render(request, self.template_name, {})
    def post(self, request, *args, **kwargs):
        login = post_parameter(request, "login")
        password = post_parameter(request, "password")
        try:
            User.objects.get(login=login) 
            return JsonResponse({"error": "Пользователь уже существует!"})
        except:
            pass

        hash_password = make_pw_hash(password)
        user = User.objects.create(username=login, password=hash_password)
        user.save()
        return redirect(reverse("main:login")) # ПОТОМ НУЖНО ИЗМЕНИТЬ ПЕРЕАДЕСАЦИЮ
        

class LogoutView(View):    
    def get(self, request, *args, **kwargs):                            
        return JsonResponse({"error": "GET method not allowed!"})
    def post(self, request, *args, **kwargs):
        del request.session["user"]
        return redirect(reverse("main:login"))


class IndexView(View):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):    
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        tasks = Task.objects.filter(user=current_user)
        
        return render(request, self.template_name, {
            "current_user": current_user,
            "tasks": tasks,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})

class TaskView(View):
    template_name = "task.html"
    def get(self, request, id):        
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        task = None                
        try:
            task = Task.objects.get(id=id)                                 
        except:
            pass   
        
        return render(request, self.template_name, {
            "task": task,                                
            "current_user": current_user,
        })
    def post(self, request, id):
        return JsonResponse({"error": "POST method not allowed!"})


class SettingsView(View):
    template_name = "settings.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        return render(request, self.template_name, {
            "test": "test",
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})


class ReservationsView(View):
    template_name = "reservations.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        return render(request, self.template_name, {
            "test": "test",
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})


class HistoryView(View):
    template_name = "history.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        return render(request, self.template_name, {
            "test": "test",
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})

# Когда в админке удаляем или обновляем фото рыбы нужно удалить ненужное фото из Яндекс бакета
@receiver(post_delete, sender=User)
def delete_user_image_ondelete(sender, instance, using, **kwargs):
    instance.image.delete(save=False)

@receiver(pre_save, sender=User)
def delete_user_image_onsave(sender, instance, using, **kwargs):
    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False    
    new_file = instance.image
    if not old_file == new_file:
        old_file.delete(save=False)