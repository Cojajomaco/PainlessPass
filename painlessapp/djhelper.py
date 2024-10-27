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
    Folder.objects.create(name="No Folder", user_id=new_user)
    return new_user

# TO-DO:
# Add randomized encryption key function, then extend instantiate user to include the function
# as a means to encrypting the PassKey.enc_key value prior to storage.
# Make sure the encryption key creation function has some static string of text to differentiate
# Between an unencrypted string and an encrypted string.
#
# Need to add a caching mechanism for user session caching. When a user signs in, the app should
# automatically use their password to unencrypt the encryption key, then store the unencrypted encryption
# key within a cache with a user configurable default timing. To start, set it to 15 minute default.
# Users should be reprompted for their password after the key expires and they attempt an unecryption
# function to access one of their passwords. 
