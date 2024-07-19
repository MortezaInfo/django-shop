from django.test import TestCase
from accounts.forms import UserRegistrationForm
from accounts.models import User

# django test form field and we don't do that

class TestRegistrationFrom(TestCase):

    @classmethod
    def setUpTestData(cls): # runing befor creation class
        User.objects.create_user(
            email = 'morteza@gmail.com',
            full_name = 'morteza nobahari',
            phone_number = '09389767293',
            password = 'mortezaaaa'
        )

    def test_valid_data(self):
        form = UserRegistrationForm(data = {'email':'mortezanobahari@email.com', 'full_name':'morteza nobahari', 'phone': '09389767292', 'password1': 'morteza:)', 'password': 'morteza:)'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5) # this form has five field
    
    def test_exist_email(self):
        # use user creation in set up data method
        form = UserRegistrationForm(data = {'email':'morteza@gmail.com', 'full_name':'morteza nobahari', 'phone': '09196558005', 'password1': 'morteza', 'password': 'morteza'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email')) #field name for error

    def test_unmatched_passwords(self):
        form = UserRegistrationForm(data = {'email':'morteza@email.com', 'full_name':'morteza nobahari', 'phone': '09389767291', 'password1': 'morteza:)', 'password': 'morteza'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)
