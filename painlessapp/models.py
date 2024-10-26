from django.conf import settings
from django.db import models


# Individual user passwords
class UserPass(models.Model):
    # name: the title for the password
    # username: username for associated password
    # password: stored password
    # uri: URI of the stored password (website)
    # folder: category for password; user created
    # user_id: user who owns the password
    name = models.CharField(max_length=255, help_text="The title of your password to "
                                                     "describe what it is.")
    username = models.CharField(max_length=255, blank=True, help_text="The username for your password.")

    # Might seem backwards to allow blank passwords in a password storage app
    # But there may be cases where a user wants to store a username or notes
    # Without actually hosting any password data
    password = models.CharField(max_length=255, blank=True, help_text="This is your password you want to store.")
    uri = models.URLField(max_length=200, blank=True, help_text="This is the website or application "
                                                                "for your password.")
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, default="None", help_text="Select one of your "
                                                                                             "folders to categorize "
                                                                                        "the password, or select none.")
    note = models.CharField(max_length=255, blank=True, help_text="This is any notes for your password. "
                                                                 "Keep it short!")
    # user_id references "settings.AUTH_USER_MODEL" which points to
    # django.contrib.auth.models.User by default; allows me to refactor
    # it later if I need to for customized authentication models.
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# Individual user folder categories
class Folder(models.Model):
    # name: title of the folder
    # user_id: user who owns the folder
    name = models.CharField(max_length=255, )
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
