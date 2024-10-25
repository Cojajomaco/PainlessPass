# Helper functions to user throughout the app.
from .models import Folder
from django.contrib.auth.models import User

# This creates the user and then also initiates default objects which require foreign key references.
# For example, user "jim" is created and a default folder model "None" is created.
# Eventually, if I get this far, this should house special encryption functions
# that assigns the user an encryption key which will be used to encrypt user passwords.
# The encryption key ideally would be encrypted by the user and stored encrypted, so only
# the user would be able to decrypt it to view their data. That's a long-shot goal, though.
def instantiate_user(username, password, email=None):
    new_user = User.objects.create_user(username, email, password)
    Folder.objects.create(name="None", user_id=new_user.id)
    return new_user
