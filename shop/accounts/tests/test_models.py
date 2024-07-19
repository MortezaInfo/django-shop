from django.test import TestCase
from accounts.models import User
#from model_bakery import bake

# for model field we don't testing! just testing mehtod!

class TestUserModel(TestCase):

    def setUp(self): # run befor all this class methods
        #self.user = bake(User, email = 'morteza@gmail.com') # overriding email field #! for available field use user.full_name command
        self.user =  User.objects.create_user(
            email = 'morteza@gmail.com',
            full_name = 'morteza nobahari',
            phone_number = '09389767293',
            password = 'mortezaaaa'
        )
        
    def test_model_str(self):
        self.assertEqual(str(self.user), 'morteza@gmail.com')