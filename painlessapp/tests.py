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
        self.assertNotEqual(User.objects.get(username="testuser").password, "testpass")
        self.assertEqual(User.objects.get(username="testuser").email, "testuser@mek-tech.net")
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
