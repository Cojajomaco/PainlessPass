import base64
import os
from django.test import TestCase
from .djhelper import instantiate_user, create_fernet_key, create_gen_enc_key, decrypt_gen_enc_key, encrypt_gen_enc_key
from django.contrib.auth.models import User
from .models import Folder, PassKey
from .models import UserPass

class UserPasswordsTestCase(TestCase):
    def test_create_user(self):
        # Create first user
        new_user = instantiate_user("testuser", "testpass", "testuser@mek-tech.net")
        # User should exist
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username="testuser").username, "testuser")
        self.assertEqual(User.objects.get(username="testuser").id, new_user.id)
        self.assertNotEqual(User.objects.get(username="testuser").password, "testpass")
        self.assertNotEqual(User.objects.get(username="testuser").email, "testuser@mek-tech.net")
        self.assertEqual(Folder.objects.get(name="No Folder", user_id=new_user.id).name, "No Folder")

    def test_create_password(self):
        new_user = instantiate_user("testuser", "testpass", "testuser@mek-tech.net")
        # Create password
        UserPass.objects.create(name="Test Pass", username="testuser", password="testpass",
                                uri="http://testurl.com", folder=Folder.objects.get(user_id=new_user),
                                note="Test note", user_id=new_user)
        self.assertTrue(UserPass.objects.filter(name="Test Pass").exists())
        self.assertTrue(UserPass.objects.filter(username="testuser").exists())
        self.assertTrue(UserPass.objects.filter(password="testpass").exists())
        self.assertTrue(UserPass.objects.filter(uri="http://testurl.com").exists())
        self.assertTrue(UserPass.objects.filter(note="Test note").exists())
        self.assertEqual(UserPass.objects.get(name="Test Pass").user_id, new_user)

    def test_create_folder(self):
        new_user = instantiate_user("testuser", "testpass", "testuser@mek-tech.net")
        # Create a folder
        Folder.objects.create(name="Test Folder", user_id=new_user)
        self.assertTrue(Folder.objects.filter(name="Test Folder").exists())
        self.assertTrue(Folder.objects.filter(user_id=new_user).exists())

    def test_create_gen_key(self):
        # Create GEKs (general encryption key)
        gek_array = []
        for i in range(10):
            gek_array.append(create_gen_enc_key())
            # Verify it contains our "unenc-" string
            self.assertIn("unenc-", gek_array[i])
            # Make sure they are long enough
            self.assertGreater(len(gek_array[i]), 120)
        # Make sure they are unique
        for i in range(0, len(gek_array)-1):
            self.assertNotEqual(gek_array[i], gek_array[i+1])

    def test_create_fernet_key(self):
        # generate salt for keys 1a/b
        salt1 = base64.b64encode(os.urandom(16)).decode("utf-8")
        # generate salt for key 2
        salt2 = base64.b64encode(os.urandom(16)).decode("utf-8")
        # verify salts are unique
        self.assertNotEqual(salt1, salt2)
        # generate password for key
        password = "sup3rs3cur3!!!"
        # token used to verify encryption is different...
        token = create_gen_enc_key()
        # create keys from salts and passwords
        key1a = create_fernet_key(salt1, password)
        key1b = create_fernet_key(salt1, password)
        key2 = create_fernet_key(salt2, password)
        # encrypt token
        enc_token1a = encrypt_gen_enc_key(key1a, token)
        enc_token1b = encrypt_gen_enc_key(key1b, token)
        enc_token2 = encrypt_gen_enc_key(key2, token)
        # decrypt encrypted tokens. dec_token1ab and dec_token1ba
        # should be equal since they use the same salt/password.
        # TODO: figure out why fernetkey is different but decryption is the same.
        # TODO: for keys generated with same salt/password
        dec_token1a = decrypt_gen_enc_key(key1a, enc_token1a)
        dec_token1ab = decrypt_gen_enc_key(key1a, enc_token1b)
        dec_token1b = decrypt_gen_enc_key(key1b, enc_token1b)
        dec_token1ba = decrypt_gen_enc_key(key1b, enc_token1a)
        dec_token2 = decrypt_gen_enc_key(key2, enc_token2)
        # verify decrypted tokens are same for 1a/b
        self.assertNotEqual(enc_token2, enc_token1b)
        self.assertEqual(dec_token1ab, dec_token1ba)
        # verify decryption works to make same original token
        self.assertEqual(dec_token1a, dec_token1b)
        self.assertEqual(dec_token1b, dec_token2)

    def test_passkey(self):
        # want to verify that users can consistently decrypt passwords stored with
        # their encrypted GEK
        user = "testuser"
        password = "testpassword"
        # create new user
        new_user = instantiate_user(user, password)
        # grab their salt
        user_salt = PassKey.objects.get(user_id=new_user.id).salt
        # verify salt exists
        self.assertIsNotNone(user_salt)
        # grab their encrypted GEK
        user_enc_gek = PassKey.objects.get(user_id=new_user.id).enc_key
        # verify enc_gek is actually encrypted using our test "unenc-" phrase
        self.assertNotIn("unenc-", user_enc_gek)
        # create Fernet object to decrypt GEk
        fernet = create_fernet_key(user_salt, password)
        # verify that the encrypted GEK can be unencrypted to include our test passphrase "unenc-"
        unenc_gek = decrypt_gen_enc_key(fernet, user_enc_gek)
        self.assertIn("unenc-", unenc_gek)
