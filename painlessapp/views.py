from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, NewPasswordForm
from .models import UserPass
from .djhelper import instantiate_user
from django import forms
from django.contrib.auth.decorators import login_required


# First page as a generic landing page.
# Should eventually prompt to log in or register.
def index(request):
    # Redirect logged-in users to their password list.
    if request.user.is_authenticated:
        return redirect("pass_list")
    context = {}
    return render(request, "painlessapp/index.html", context)


# This page should be the user's homepage which includes a
# list of all of their passwords, along with a navbar for other services
# such as password generation, settings, and logging out.
def home(request):
    # Redirect logged-in users to their password list.
    if request.user.is_authenticated:
        return redirect("pass_list")
    context = {}
    return render(request, "painlessapp/home.html", context)


# Register page, also straightforward.
# IT should also include a prompt to sign in if you have an account.
def register(request):
    # Redirect logged-in users to their password list.
    if request.user.is_authenticated:
        return redirect("pass_list")
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
            # This actually creates the user and initiates some important objects.
            instantiate_user(new_username, new_pass)
            user = authenticate(username=new_username, password=new_pass)
            login(request, user)
            return redirect('home')

    else:
        register_form = RegistrationForm()
    context = {'register_form': register_form}
    return render(request, "painlessapp/register.html", context)


@login_required
def pass_list(request):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")
    # Filter list to ONLY current user objects.
    userpass_list = UserPass.objects.filter(user_id=request.user)
    context = {"userpass_list": userpass_list}
    return render(request, "painlessapp/pass_list.html", context)


# This should return the user's individual password entry.
# Ideally it'd be a pop-out, but, alas, new developer.
@login_required
def pass_entry(request, pass_id):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")
    # Make sure user can access the pass_id
    userpass_entry = UserPass.objects.get(pk=pass_id)
    if userpass_entry.user_id != request.user:
        return HttpResponse('Unauthorized', status=401)
    context = {
        "userpass_entry": userpass_entry,
    }
    return render(request, "painlessapp/pass_entry.html", context)


@login_required
def pass_new(request):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")

    if request.method == 'POST':
        # Create the form object to validate data
        password_form = NewPasswordForm(request.POST, user_id=request.user)
        if password_form.is_valid():
            # Set user_id (owner) of object to the logged in user.
            password_form.instance.user_id = request.user

            # TODO: Encrypt password prior to storage
            # Save the UserPass model after validating the form.
            new_pass = password_form.save()
            return redirect('/painlesspass/pass_entry/' + str(new_pass.pk))

    else:
        # Creates password form and feeds the currently logged-in user as an argument.
        password_form = NewPasswordForm(user_id=request.user)
    context = {"password_form": password_form}
    return render(request, "painlessapp/pass_new.html", context)


# Settings page for individual user setting configuration.
@login_required
def settings(request):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")
    context = {}
    return render(request, "painlessapp/settings.html", context)
