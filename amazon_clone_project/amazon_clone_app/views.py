from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView
from django.shortcuts import redirect
from . import models

# DashBoardView
class DashBoardView(TemplateView):
    template_name = "amazon_clone_app/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if models.CustomUser.objects.get(id = user.id):
            context["user"] = f"Welcome {user.first_name}"
            return context
        return None
    
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