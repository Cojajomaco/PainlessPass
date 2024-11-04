from django.urls import path
from . import views

urlpatterns = [
    # HTML FILES
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("signin/", views.signin, name="signin"),
    path("register/", views.register, name="register"),
    path("pass_list/", views.pass_list, name="pass_list"),
    path("pass_entry/<int:pass_id>/", views.pass_entry, name="pass_entry"),
    path("settings/", views.settings, name="settings"),
    # API REQUESTS
]
