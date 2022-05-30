from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.dispatch import receiver
from django.db.models.signals import *
from grpc import Status

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
    roles = ["user"]
    def get(self, request, *args, **kwargs):    
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        if current_user.role.name not in self.roles:
             return redirect(reverse("main:manager_tasks"))
        tasks = Task.objects.filter(user=current_user).order_by("status")
        
        status = get_parameter(request, "status")
        if status:
            tasks = tasks.filter(status=status)

        return render(request, self.template_name, {
            "current_user": current_user,
            "tasks": tasks,
            "status": status,
            "statuses": TASK_STATUS,
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
            
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})


class ProjectsView(View):
    template_name = "projects.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        tasks = Task.objects.filter(user=current_user)
        projects = Project.objects.all()
        if current_user.role.name == 'user':
            projects = Project.objects.filter(tasks__in=tasks)
        return render(request, self.template_name, {            
            "projects": projects,
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})

class AddProjectView(View):
    roles = ["manager"]
    template_name = "add_project.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        if current_user.role.name not in self.roles:
             return redirect(reverse("main:index"))
        technologies = Technology.objects.all()        
        return render(request, self.template_name, {            
            "technologies": technologies,
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        name = post_parameter(request, "name")
        description = post_parameter(request, "description")
        start_date = post_parameter(request, "start-date")
        end_date = post_parameter(request, "end-date")
        tasks = post_parameter(request, "tasks")
        
        tasks = json.loads(tasks)        
        model_tasks = []
        
        for task in tasks:            
            technologies = task["technologies"]
            model_technologies = Technology.objects.filter(name__in=technologies)
            model_task = Task.objects.create(name=task["name"], description=task["description"], start_date=task["start-date"], end_date=task["end-date"])
            for item in model_technologies:
                model_task.technologies.add(item)
            model_task.save()
            model_tasks.append(model_task)
        project = Project.objects.create(name=name, description=description, start_date=start_date, end_date=end_date)
        for item in model_tasks:
            project.tasks.add(item)
        project.save()
        return JsonResponse({"message": "Вы успешно добавили проект!"}, status=200)

class HistoryView(View):
    template_name = "history.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        return render(request, self.template_name, {
            
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})

class TasksView(View):
    roles = ["manager"]
    template_name = "manager-tasks.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        if current_user.role.name not in self.roles:
            return redirect(reverse("main:index"))

        worker_role = get_or_none(Role, name="user")

        status = get_parameter(request, "status")
        #status = "" if status == "" else status

        project_id = get_parameter(request, "project")
        project = get_or_none(Project, id=project_id)

        worker_id = get_parameter(request, "worker")
        worker = get_or_none(User, id=worker_id)        

        tasks = Task.objects.order_by("status")
        if status:
            tasks = Task.objects.filter(status=status)    
        if project:
            tasks = tasks.filter(id__in=project.tasks.all())
        if worker:
            tasks = tasks.filter(user=worker)

        #statuses = get_status_list()
        return render(request, self.template_name, {
            "tasks": tasks,
            "current_user": current_user,
            "statuses": TASK_STATUS,
            "status": status,
            "current_project": project,
            "projects": Project.objects.all(),
            "workers": User.objects.filter(role=worker_role),
            "current_worker": worker,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})

class AddTaskView(View):
    roles = ["manager"]
    template_name = "add_task.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        if current_user.role.name    not in self.roles:
            return redirect(reverse("main:index"))        
        return render(request, self.template_name, {            
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return JsonResponse({"error": "Вы не вошли в систему!"}, status=500)
        if current_user.role not in self.roles:
            return JsonResponse({"error": "У вас нет прав на добавление!"}, status=500)

        project_id = post_parameter(request, "project")
        project = get_or_none(Project, id=project_id)
        if not project:
            return JsonResponse({"error": "Проект с таким id не найден!"}, status=500)
        
        user_id = post_parameter(request, "user")
        user = get_or_none(User, id=user_id)
        if not user:
            return JsonResponse({"error": "Юзер с таким id не найден!"}, status=500)

        name = post_parameter(request, "name")
        description = post_parameter(request, "description")        
        start_date = post_parameter(request, "start_date")
        end_date = post_parameter(request, "end_date")
        technologies = post_parameter(request, "technologies")

        task = Task.objects.create(name=name, description=description, user=user, start_date=start_date, end_date=end_date, technologies=technologies)
        task.save()
        project.tasks.add(task)
        project.save()
        return JsonResponse({"success": True, "message": "Вы успешно добавили задачу!"}, status=200)

class AddWorkerView(View):
    roles = ["manager"]
    template_name = "add_worker.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))        
        if current_user.role.name not in self.roles:
            return redirect(reverse("main:index"))        
        technologies = Technology.objects.all()
        return render(request, self.template_name, {            
            "current_user": current_user,
            "technologies": technologies,
        })
    def post(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return JsonResponse({"error": "Вы не вошли в систему!"}, status=500)
        if current_user.role.name not in self.roles:
            return JsonResponse({"error": "У вас нет прав на добавление!"}, status=500)                

        full_name = post_parameter(request, "name")
        work_exp = post_parameter(request, "work_exp")        
        telegram = post_parameter(request, "telegram")
        vk = post_parameter(request, "vk")
        phone = post_parameter(request, "phone")
        password = post_parameter(request, "password")
        login = post_parameter(request, "login")
        technologies = post_parameter(request, "technologies")
        
        technologies = technologies.split(",")
        model_technologies = Technology.objects.filter(name__in=technologies)

        worker = User.objects.create(full_name=full_name, work_experience=work_exp, telegram=telegram, vk=vk, phone=phone, username=login, password=password)
        for item in model_technologies:
            worker.technologies.add(item)
        worker.save()
        
        return JsonResponse({"success": True, "message": "Вы успешно добавили работника!"}, status=200)



class WorkersView(View):
    template_name = "workers.html"
    def get(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        worker_role = Role.objects.get(name="user")
        workers = User.objects.filter(role=worker_role)
        return render(request, self.template_name, {
            "workers": workers,
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})

class DeleteWorkersView(View):    
    roles = ["manager"]
    def get(self, request, id):
        return JsonResponse({"error": "POST method not allowed!"})
    def post(self, request, id):
        worker = get_or_none(User, id=id)
        
        if not worker:
            return redirect(reverse("main:workers"))
        current_user = get_current_user(request)
        if current_user.role.name not in self.roles:
            return redirect(reverse("main:workers"))
        
        worker.delete()
        return redirect(reverse("main:workers"))
        

class UpdateAvatar(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse("main:index"))
    def post(self, request, *args, **kwargs):
        image = request.FILES.get("image", None)
        if not image:
            return JsonResponse({"error": "Не передано изображение!"}, status=500)
        
        if(check_image_type(image) and image):
            current_user = get_current_user(request)
            if not current_user:
                return JsonResponse({"error": "Пользователь не найден!"})
            current_user.image = image
            current_user.save()
            return JsonResponse({"image": current_user.image.url}, status=200)
        else:            
            return JsonResponse({"error": "Выберите .jpg, .jpeg или .png формат!"}, status=500)


class SetTaskStatus(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse("main:index"))
    def post(self, request, id):
        task = get_or_none(Task, id=id)        
        if not task:
            return JsonResponse({"error": "Задача с таким id не найдена!"}, status=500)
        
        status = post_parameter(request, "status")
        task.status = status
        task.save()        
        return redirect(reverse("main:index"))

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