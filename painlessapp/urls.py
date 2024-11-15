from django.urls import path
from . import views

urlpatterns = [
    # HTML FILES
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("pass_list/", views.pass_list, name="pass_list"),
    path("pass_entry/<int:pass_id>/", views.pass_entry, name="pass_entry"),
    path("pass_new/", views.pass_new, name="pass_new"),
    path("settings/", views.settings, name="settings"),
    path("folder_list/", views.folder_list, name="folder_list"),
    path("folder_entry/<int:folder_id>/", views.folder_entry, name="folder_entry"),
    path("folder_new/", views.folder_new, name="folder_new"),
    # API REQUESTS
]
