from django.conf import settings
from django.db import models


# Individual user folder categories
class Folder(models.Model):
    # name: title of the folder
    # user_id: user who owns the folder
    name = models.CharField(max_length=255)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Make the choice names pretty and give it a string representation.
    def __str__(self):
        return self.name


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
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, help_text="Select one of your folders "
                                                                           "to categorize the password, or "
                                                                           "select none.")
    note = models.CharField(max_length=255, blank=True, help_text="This is any notes for your password. "
                                                                  "Keep it short!")
    # user_id references "settings.AUTH_USER_MODEL" which points to
    # django.contrib.auth.models.User by default; allows me to refactor
    # it later if I need to for customized authentication models.
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Make the choice names pretty and give it a string representation.
    def __str__(self):
        return self.name


# To-Do:
# Extend the user class.
# The extension should store an encryption key.
# This encryption key will be used to encrypt each password in the database.
# The encryption key will be encrypted by the user's actual password (not the hash).
# Need to implement + test encryption of incoming passwords via the "storedKey".
# Then implement the encryption and decryption of the key during runtime.
class PassKey(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    salt = models.CharField(max_length=32)
    enc_key = models.TextField()
