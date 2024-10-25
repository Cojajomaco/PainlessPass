from django.test import TestCase
from .djhelper import instantiate_user
from django.contrib.auth.models import User
from .models import Folder
from .models import UserPass

class UserPasswordsTestCase(TestCase):
    def test_create_user(self):
        # Create first user
        new_user = instantiate_user("testuser", "testpass", "testuser@mek-tech.net")
        # User should exist
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username="testuser").username, "testuser")
        self.assertEqual(User.objects.get(username="testuser").id, new_user.id)
        self.assertEqual(User.objects.get(username="testuser").password, "testpass")
        self.assertEqual(User.objects.get(username="testuser").email, "testuser@mek-tech.net")
        # Default folder object for the user should be created.
        self.assertTrue(Folder.objects.exists(name="None", user_id=new_user.id))

    def test_create_password(self):
        new_user = instantiate_user("testuser", "testpass", "testuser@mek-tech.net")
        # Create password
        UserPass.objects.create(name="Test Pass", username="testuser", password="testpass",
                                           uri="http://testurl.com", note="Test note",
                                           user_id=new_user)
        self.assertTrue(UserPass.objects.exists(name="Test Pass"))
        self.assertTrue(UserPass.objects.exists(username="testuser"))
        self.assertTrue(UserPass.objects.exists(password="testpass"))
        self.assertTrue(UserPass.objects.exists(uri="http://testurl.com"))
        self.assertTrue(UserPass.objects.exists(note="Test note"))
        self.assertEqual(UserPass.objects.get(name="Test Pass").user_id, new_user.id)

    def test_create_folder(self):
        new_user = instantiate_user("testuser", "testpass", "testuser@mek-tech.net")
        # Create a folder
        Folder.objects.create(name="Test Folder", user_id=(User.objects.get(username="testuser")).id)
        self.assertTrue(Folder.objects.exists(name="Test Folder"))
        self.assertTrue(Folder.objects.exists(user_id=new_user))