from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Task
from .forms import FormRegistrationClass

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from django.contrib.auth import views as auth_views

# Create your views here.
class UserRegistration(FormView):
    template_name = "main/register.html"
    success_url = reverse_lazy("tasks-view")
    form_class = FormRegistrationClass

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)       #this method logs in a user automatically 
        return super(UserRegistration, self).form_valid(form)

    #redirect authenticated users to the tasks view page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("tasks-view")
        return super(UserRegistration, self).get(*args, **kwargs)

class UserLogin(LoginView):
    template_name = "main/login.html"
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy("tasks-view")

#classes for password reset
class CustomPasswordReset(auth_views.PasswordResetView):
    template_name = "main/password/password_reset.html"
    def __str__(self):
        return self

class CustomPasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = "main/password/password_reset_done.html"
    def __str__(self):
        return self

class CustomPasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = "main/password/password_reset_confirm.html"
    def __str__(self):
        return self

class CustomPasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = "main/password/password_reset_complete.html"
    def __str__(self):
        return self



class TasksView(LoginRequiredMixin, ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = context["object_list"].filter(user=self.request.user)
        context["number_of_complete_tasks"] = context["object_list"].filter(complete=True).count()
        context["number_of_incomplete_tasks"] = context["object_list"].filter(complete=False).count()
        search_input = self.request.GET.get("user-search-input") or ""
        if search_input:
            context["object_list"] = context["object_list"].filter(title__icontains=search_input)
        return context



class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("tasks-view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)

class EditTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "complete"]
    template_name = "main/edit.html"
    success_url = reverse_lazy("tasks-view")

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "main/delete.html"
    success_url = reverse_lazy("tasks-view")