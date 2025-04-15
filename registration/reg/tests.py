from django.test import TestCase
from django.contrib.auth.models import User

from registration.reg.utils import create_unique_code_for_user


# Create your tests here.

class UserCodeTestCase(TestCase):
    def test_code_generation(self):
        user = User.objects.create(username="test_user")
        code1 = create_unique_code_for_user(user)
        code2 = create_unique_code_for_user(User.objects.create(username="test_user2"))
        self.assertNotEqual(code1.code, code2.code)