from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, NewPasswordForm, NewFolderForm
from .models import UserPass, Folder
from .djhelper import instantiate_user, decrypt_and_store_key, encrypt_user_pass, decrypt_user_pass
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, logout
from django.http import HttpResponseRedirect
from django.utils import timezone
import random
import linecache

# Wordlist and its length
wordlist = "google-5000-english-usa-no-swears-medium.txt"
wordlist_length = 5000

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

                # If passwords don't match, redirect with error message explaining
                messages.info(request, "Passwords do not match.")
                return redirect('register')

            # This actually creates the user and initiates some important objects.
            instantiate_user(new_username, new_pass)
            user = authenticate(username=new_username, password=new_pass)

            # Get user password, decrypt GEK, store in volatile cache
            decrypt_and_store_key(user, new_pass)
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

    # Returns passwords by their name to order them.
    userpass_list = userpass_list.order_by('name')
    userfolder_list = Folder.objects.filter(user_id=request.user)
    context = {"userpass_list": userpass_list,
               "userfolder_list": userfolder_list}

    return render(request, "painlessapp/pass_list.html", context)


# This should return the user's individual password entry.
# Ideally it'd be a pop-out, but, alas, new developer.
@login_required
def pass_entry(request, pass_id):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")

    # TODO: Customize timezones based on a Settings model which stores timezones
    timezone.activate('America/Chicago')

    # Lets the view know that the entry was not updated yet; POST statement resolves this to True if needed
    entry_updated = False

    # Grab user GEK for potential use in FKEY generation for encryption
    user_GEK = cache.get(str(request.user) + "-GEK")

    # Check if GEK is available from the cache for encryption. If not, prompt for login...
    if user_GEK is None:
        logout(request)
        return redirect('/painlesspass/login/')

    # Make sure user can access the pass_id; 404 if not available
    userpass_entry = get_object_or_404(UserPass, pk=pass_id, user_id=request.user)
    userpass_entry.password = decrypt_user_pass(request.user.id, userpass_entry.password)
    if userpass_entry.user_id != request.user:
        return HttpResponse('Unauthorized', status=401)

    password_form = NewPasswordForm(user_id=request.user, instance=userpass_entry)

    if request.method == 'POST':

        # Create the form object to validate data
        password_form = NewPasswordForm(request.POST, user_id=request.user, instance=userpass_entry)
        if password_form.is_valid():

            # Pass to function that does the encryption
            enc_NewPass = encrypt_user_pass(request.user.id, password_form.clean().get('password'))

            # Save the UserPass model after validating the form and adding encrypted password.
            new_pass = password_form.save(commit=False)
            new_pass.password = enc_NewPass
            new_pass.save()

            # Lets the view know that the entry was updated
            entry_updated = True


    context = {
        "userpass_entry": userpass_entry,
        "userpass_form": password_form,
        "entry_updated": entry_updated,
    }
    return render(request, "painlessapp/pass_entry.html", context)


@login_required
def pass_new(request):

    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")

    # Grab user GEK for potential use in FKEY generation for encryption
    user_GEK = cache.get(str(request.user) + "-GEK")

    # Check if GEK is available from the cache for encryption. If not, prompt for login...
    if user_GEK is None:
        logout(request)
        return redirect('/painlesspass/login/')

    if request.method == 'POST':

        # Create the form object to validate data
        password_form = NewPasswordForm(request.POST, user_id=request.user)
        if password_form.is_valid():

            # Set user_id (owner) of object to the logged-in user.
            password_form.instance.user_id = request.user

            # Pass to function that does the encryption
            enc_NewPass = encrypt_user_pass(request.user.id, password_form.clean().get('password'))

            # Save the UserPass model after validating the form and adding encrypted password.
            new_pass = password_form.save(commit=False)
            new_pass.password = enc_NewPass
            new_pass.save()

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


# Call to create a folder.
@login_required
def folder_new(request):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")

    # Create the folder form object. If it's a GET operation, it will be empty.
    # A POST operation will modify the form and return based on modifications.
    folder_form = NewFolderForm()

    if request.method == 'POST':
        # Create the form object to validate data
        folder_form = NewFolderForm(request.POST)
        if folder_form.is_valid():

            # Form Error Cases
            # Saving cleaned name for use in error checks
            new_folder_name = folder_form.cleaned_data['name']

            # Prevent naming folder "No Folder"
            if new_folder_name == "No Folder":
                folder_form.add_error('name', 'The folder cannot be titled "No Folder".')

            # Checking for a folder that violates unique name per user Folder model constraint
            if Folder.objects.filter(name=new_folder_name, user_id=request.user).exists():
                folder_form.add_error('name', 'A folder already exists with that name.')

            # Set user_id (owner) of object to the logged-in user.
            folder_form.instance.user_id = request.user

            # Verify there are no errors in the form, then save and return a successful page
            if len(folder_form.errors) == 0:
                new_folder = folder_form.save()
                return redirect('/painlesspass/folder_entry/' + str(new_folder.pk))

    context = {"folder_form": folder_form}
    return render(request, "painlessapp/folder_new.html", context)


# Lists folders.
@login_required
def folder_list(request):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")

    # TODO: Customize timezones based on a Settings model which stores timezones
    timezone.activate('America/Chicago')

    # Filter list to ONLY current user objects.
    userfolder_list = Folder.objects.filter(user_id=request.user)

    # Returns folders by name to order them.
    userfolder_list = userfolder_list.order_by('name')
    context = {"userfolder_list": userfolder_list}
    return render(request, "painlessapp/folder_list.html", context)


# Show specific folder entry.
@login_required
def folder_entry(request, folder_id):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")

    # Make sure user can access the folder; 404 if not available
    userfolder_entry = get_object_or_404(Folder, pk=folder_id, user_id=request.user)
    if userfolder_entry.user_id != request.user:
        return HttpResponse('Unauthorized', status=401)

    # TODO: Customize timezones based on a Settings model which stores timezones
    timezone.activate('America/Chicago')

    # Lets the view know that the entry was not updated yet; POST statement resolves this to True if needed
    entry_updated = False

    # Form with the object data
    userfolder_form = NewFolderForm(instance=userfolder_entry)

    # Handling processing for an edit request to the Folder data
    if request.method == 'POST':
        # Create the form object to validate data
        userfolder_form = NewFolderForm(request.POST, instance=userfolder_entry)
        if userfolder_form.is_valid():

            # Form Error Cases
            # Saving cleaned name for use in error checks
            new_folder_name = userfolder_form.cleaned_data['name']
            # Prevent naming folder "No Folder"
            if new_folder_name == "No Folder":
                userfolder_form.add_error('name', 'The folder cannot be titled "No Folder".')

            # Checking for a folder that violates unique name per user Folder model constraint
            if Folder.objects.filter(name=new_folder_name, user_id=request.user).exists():
                userfolder_form.add_error('name', 'A folder already exists with that name.')

            # Verify there are no errors in the form, then save and return a successful page
            if len(userfolder_form.errors) == 0:
                userfolder_form.save()

                # Lets the view know that the entry was updated
                entry_updated = True

    context = {
        "userfolder_entry": userfolder_entry,
        "userfolder_form": userfolder_form,
        "entry_updated": entry_updated,
    }
    return render(request, "painlessapp/folder_entry.html", context)


# Delete folder
@login_required
def folder_delete(request, folder_id):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")

    # Make sure user can access the folder
    userfolder_entry = Folder.objects.get(pk=folder_id, user_id=request.user)
    if userfolder_entry.user_id != request.user:
        return HttpResponse('Unauthorized', status=401)
    elif userfolder_entry.user_id == request.user:

        # Can't delete No Folder item
        if userfolder_entry.name == "No Folder":
            return HttpResponse('Unauthorized', status=401)

        # Change all password with deleted folder to "No Folder" object
        pass_change_folders = UserPass.objects.filter(folder=userfolder_entry, user_id=request.user)
        no_folder = Folder.objects.get(user_id=request.user, name="No Folder")
        pass_change_folders.update(folder=no_folder)
        userfolder_entry.delete()

    return redirect("/painlesspass/folder_list")


# Delete password
@login_required
def pass_delete(request, pass_id):
    # Redirect logged-out users to the signin page.
    if not request.user.is_authenticated:
        return redirect("/accounts/login")

    # Make sure user can access the pass_id
    userpass_entry = UserPass.objects.get(pk=pass_id, user_id=request.user)
    if userpass_entry.user_id != request.user:
        return HttpResponse('Unauthorized', status=401)
    elif userpass_entry.user_id == request.user:
        userpass_entry.delete()

    return redirect("/painlesspass/pass_list")


# Overrides a specific function in the login view class that, once a user is authenticated,
# uses their password to decrypt their general encryption key (GEK) and store it in a cached,
# volatile memory variable.
class CustomLoginView(LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())

        # Get user password, decrypt GEK, store in volatile cache for usage in encryption functions
        decrypt_and_store_key(self.request.user, form.clean().get('password'))
        return HttpResponseRedirect(self.get_success_url())

# Generates a password based on user specified password generation settings.
def pass_gen(request):

    # Password we will build from the wordlist
    generated_password = ""

    # TODO: Let this be updated with user variables
    # Amount of words to use in password
    num_words = 3

    # Should first letter be capitalized
    uppercase = True

    # Should a number be added
    use_number = True

    # If a number should be added, determine where
    if use_number:
        number_added_word = random.randint(0, num_words - 1)
    else:
        number_added_word = -1


    # Get number of words, add to password, and separate them. Sprinkle in a number.
    curr_word = 0
    while curr_word < num_words:

        # Find a word to grab from the list
        grab_word_num = random.randint(0, wordlist_length -1)

        # Grab it, clean it a bit, and add numbers, capitals, or hyphens as needed for the phrase
        line = linecache.getline(wordlist, grab_word_num)
        line = line.replace("\n", "")
        if uppercase:
            line = line.capitalize()
        generated_password += line
        if curr_word == number_added_word:
            generated_password += str(random.randint(0, 9))

        # If we aren't the last word, add a hyphen to the phrase
        if curr_word != (num_words - 1):
            generated_password += "-"

        curr_word += 1

    # Response to return in JSON format
    pass_json = {
        'gen_password': generated_password,
    }

    return JsonResponse(pass_json)
