from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashBoardView.as_view(), name="dashboard"),
    path("register/", views.RegisterView.as_view(), name="register")
]