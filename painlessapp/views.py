from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm
from .djhelper import instantiate_user
from django import forms


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
    # If user submits a POST request to /register/, try to create account.
    if request.method == 'POST':
        # Create the form object to validate data
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            # Grab user data
            new_username = register_form.cleaned_data['username']
            # Check username isn't taken
            if User.objects.filter(username=new_username).exists():
                messages.info(request, "Username is taken.")
                return redirect('register')
            # Try to grab new password
            try:
                new_pass = register_form.clean_password2()
            except forms.ValidationError:
                messages.info(request, "Passwords do not match.")
                return redirect('register')
            instantiate_user(new_username, new_pass)
            user = authenticate(username=new_username, password=new_pass)
            login(request, user)
            return redirect('home')

    else:
        register_form = RegistrationForm()
    context = {'register_form': register_form}
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
