from django.shortcuts import render
from django.http import HttpResponse

# First page as a generic landing page.
# Should eventually prompt to log in or register.
def index(request):
    return HttpResponse("painlesspass index.")

# This page should be the user's homepage which includes a
# list of all of their passwords, along with a navbar for other services
# such as password generation, settings, and logging out.
def home(request):
    return HttpResponse("painlesspass home.")

# Sign-in page, should be straightforward what it does.
# It should also include a prompt to register for an account.
def signin(request):
    return HttpResponse("painlesspass signin.")

# Register page, also straightforward.
# IT should also include a prompt to sign in if you have an account.
def register(request):
    return HttpResponse("painlesspass register.")

# This should return the user's individual password entry.
# Ideally it'd be a pop-out, but, alas, new developer.
def password(request):
    return HttpResponse("painlesspass pass.")

