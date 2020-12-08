from django.core.management import CommandError, call_command
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from user.apps import UserConfig
from user.models import User


class UserManagerTestCase(TestCase):
    email = "tester@debugwith.me"
    username = "tester"

    def test_apps(self):
        self.assertEqual(UserConfig.name, "user")

    def test_create_user(self):
        user = User.objects.create_user(username=self.username, email=self.email, password="test")
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertTrue(user.has_usable_password())
        self.assertEqual(user.__str__(), self.username)
        self.assertEqual(user.full_name, self.username)
        self.assertTrue(isinstance(user.created_at, type(timezone.now())))
        user.first_name = "Testing"
        user.last_name = "Dummy"
        user.save()
        self.assertNotEqual(user.full_name, self.username)

    def test_unique_user_username(self):
        username = self.username + "1"
        User.objects.create_user(username=username, email=self.email)
        self.assertRaises(IntegrityError, User.objects.create_user, username=username)

    def test_create_superuser(self):
        self.assertRaises(
            ValueError,
            User.objects.create_superuser,
            username="any_test_name",
            is_staff="abc",
        )
        self.assertRaises(
            ValueError,
            User.objects.create_superuser,
            username="any_test_name",
            is_superuser=False,
        )

    def test_empty_username(self):
        self.assertRaises(TypeError, User.objects.create_user, email=self.email)
        self.assertRaises(ValueError, User.objects.create_user, email=self.email, username=None)

    def test_empty_email(self):
        user = User.objects.create_user(username=self.username)
        self.assertEqual(user.email, "")

    def test_empty_password(self):
        user = User.objects.create_user(email=self.email, username=self.username)
        self.assertFalse(user.has_usable_password())

    def test_custom_create_command(self):
        with self.settings(DEFAULT_ADMIN_USERNAME=None):
            with self.assertRaises(CommandError) as exc:
                call_command("initadmin")

        self.assertTrue("Default admin details are not set!" in exc.exception.args)

        with self.settings(
            DEFAULT_ADMIN_USERNAME="testadm", DEFAULT_ADMIN_EMAIL="testadm@debugwith.me", DEFAULT_ADMIN_PASS="testpass"
        ):
            call_command("initadmin")
            self.assertTrue(User.objects.filter(username="testadm").exists(), msg="User is not created.")
            user = User.objects.get(username="testadm")
            self.assertTrue(user.has_usable_password())
            self.assertEqual(user.username, "testadm")
            self.assertEqual(user.email, "testadm@debugwith.me")
            self.assertTrue(user.check_password("testpass"))
            # calling the command twice should not cause an issue
            call_command("initadmin")
