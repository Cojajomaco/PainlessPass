from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# First page as a generic landing page.
# Should eventually prompt to log in or register.
def index(request):
    context = {}
    return render(request, "painlessapp/index.html", context)


# This page should be the user's homepage which includes a
# list of all of their passwords, along with a navbar for other services
# such as password generation, settings, and logging out.
def home(request):
    context = {}
    return render(request, "painlessapp/home.html", context)


# Sign-in page, should be straightforward what it does.
# It should also include a prompt to register for an account.
def signin(request):
    context = {}
    return render(request, "painlessapp/signin.html", context)


# Register page, also straightforward.
# IT should also include a prompt to sign in if you have an account.
def register(request):
    context = {}
    return render(request, "painlessapp/register.html", context)


def pass_list(request):
    context = {}
    return render(request, "painlessapp/pass_list.html", context)


# This should return the user's individual password entry.
# Ideally it'd be a pop-out, but, alas, new developer.
def pass_entry(request, pass_id):
    context = {
        "pass_id": pass_id,
    }
    return render(request, "painlessapp/pass_entry.html", context)

# Settings page for individual user setting configuration.
def settings(request):
    context = {}
    return render(request, "painlessapp/settings.html", context)
