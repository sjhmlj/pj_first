from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("profile_update/", views.profile_update, name="profile_update"),
    path("password_update/", views.password_update, name="password_update"),
    path("delete/", views.delete, name="delete"),
]
