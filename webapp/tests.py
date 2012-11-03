"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

# Login test case
class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        User.objects.create_user('Fake Name', 'fake@dartmouth.edu', 'password')

        # perform login and check
        #user = self.client.login(username='Fake Name', password='mypassword')

        user = self.client.login(username='Fake Name', password='password')
        self.assertTrue(user)
