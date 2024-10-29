# Helper functions to user throughout the app.
from .models import Folder, PassKey
from django.contrib.auth.models import User
import secrets
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# TO-DO:
# Add randomized encryption key function, then extend instantiate user to include the function
# as a means to encrypting the PassKey.enc_key value prior to storage. The default, for now, has "unenc-"
# pre-pended to it for testing to know between the unencrypted and encrypted variants.
def create_gen_enc_key():
    gen_enc_key = "unenc-" + secrets.token_urlsafe(120)
    return gen_enc_key


# Takes user's salt and creates an instance of Fernet used to decrypt or encrypt later
def create_fernet_key(salt, password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password, encoding="utf-8")))
    return Fernet(key)


# Takes input of (Fernet, token) to encrypt the token.
def encrypt_gen_enc_key(fernetkey, token):
    enc_token = fernetkey.encrypt(bytes(token, encoding="utf-8"))
    return enc_token.decode("utf-8")


# Takes input of (Fernet, token) to decrypt the token.
def decrypt_gen_enc_key(fernetKey, token):
    dec_token = fernetKey.decrypt(bytes(token, encoding="utf-8"))
    return dec_token.decode("utf-8")


# This creates the user and then also initiates default objects which require foreign key references.
# For example, user "jim" is created and a default folder model "None" is created.
# Eventually, if I get this far, this should house special encryption functions
# that assigns the user an encryption key which will be used to encrypt user passwords.
# The encryption key ideally would be encrypted by the user and stored encrypted, so only
# the user would be able to decrypt it to view their data. That's a long-shot goal, though.
def instantiate_user(username, password, email=None):
    # Create new user
    new_user = User.objects.create_user(username, email, password)

    # Create encryption key
    salt = os.urandom(16)
    fernet_key = create_fernet_key(salt, password)
    gen_enc_key = create_gen_enc_key()
    enc_token = encrypt_gen_enc_key(fernet_key, gen_enc_key)
    PassKey.objects.create(user_id=new_user, salt=salt, enc_key=enc_token)

    # Create default folder
    Folder.objects.create(name="No Folder", user_id=new_user)
    return new_user