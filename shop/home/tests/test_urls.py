from django.test import SimpleTestCase # we can use TestCase
from django.urls import reverse, resolve
from home.views import HomeSearchView

# here just search us urls redirect to class view ?
class TestUrls(SimpleTestCase):

    def test_home_view(self): # just test one something
        url = reverse('home:search', args=('tishirt',)) 
        self.assertEqual(resolve(url).func.view_class, HomeSearchView)

        
    