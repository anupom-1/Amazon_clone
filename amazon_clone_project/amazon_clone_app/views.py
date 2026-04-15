from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView, FormView
from django.shortcuts import redirect
from . import models
from django.views import View
from django.contrib.auth import authenticate,logout, login
from django.urls import reverse
from django.shortcuts import redirect
from . import forms

# DashBoardView
class DashBoardView(TemplateView):
    template_name = "amazon_clone_app/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if models.CustomUser.objects.filter(id = user.id).exists():
            context["user"] = f"Welcome {user.first_name}"
            return context
        return context
    
# RegisterView
class RegisterView(CreateView):
    model = models.CustomUser
    success_url = "/"
    fields = ["first_name", "last_name", "email", "password", "gender", "account_type"]
    template_name = "amazon_clone_app/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data["password"]
        if password:
            user.set_password(password)
        user.save()
        models.Profile.objects.create(user=user)
        self.object = user
        return redirect(self.success_url) 
    
class LogInView(FormView):
    template_name = "amazon_clone_app/login.html"
    form_class = forms.LoginForm
    # initial = None
    # success_url = "dashboard"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = self.request.POST.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            models.Profile.objects.get_or_create(user=user)
            return redirect("dashboard")
        form.add_error(None, "invalid email or password")
        return self.form_invalid(form)

# LogOutView   
class LogOutView(View):

    def post(self, request):
        logout(request)
        return redirect("login")


