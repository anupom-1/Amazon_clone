from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashBoardView.as_view(), name="dashboard"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LogInView.as_view(), name="login"),
    path("logout/", views.LogOutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/post/", views.PostCreateView.as_view(), name="post"),
]