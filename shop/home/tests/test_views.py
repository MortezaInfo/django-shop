from django.test import TestCase, Client
from home.forms import CommentReplyForm, CommentCreateForm
from order.forms import CartAddForm
from accounts.models import User
from home.models import Comment, Category, Products
from django.urls import reverse


class TestProductDetailViews(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email = 'morteza@gmail.com',
            full_name = 'morteza N',
            phone_number = '09389767293',
            password = 'morteza info'
        )
        
        self.client = Client()
        self.category = Category.objects.create(name = 'cloth', slug = 'cloth')
        self.product = Products.objects.create(name = 't-shirt', slug = 't-shirt', price = 22, id = 1)
        self.product.category.set([self.category])
        
    def test_product_detail_GET(self):
        response = self.client.get(reverse('home:product_detail', args=[self.category.slug, self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/detail.html')
        self.failUnless(response.context['form'], CommentCreateForm)
        self.failUnless(response.context['reply_form'], CommentReplyForm)
        self.failUnless(response.context['form_quantity'], CartAddForm)
    
    def test_product_detail_POST_valid(self):
        self.client.login(
            email = 'morteza@gmail.com',
            phone_number = '09389767293',
            password = 'morteza info'
        )
        
    
        response = self.client.post(reverse('home:product_detail', args=[self.category.slug, self.product.id]), data = {'body':'this is comment for this post'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(reverse('home:product_detail', args=[self.category.slug, self.product.id]))
        self.assertEqual(Comment.objects.count(), 1)
    
    def test_product_detail_POST_invalid(self):
        self.client.login(
            email = 'morteza@gmail.com',
            phone_number = '09389767293',
            password = 'morteza info'
        )
    
        response = self.client.post(reverse('home:product_detail', args=[self.category.slug, self.product.id]), data = {'body':False})
        self.assertEqual(response.status_code, 302)
        self.failIf(response.context['form'].is_vaild())
        self.assertFormError(response.context['form'], field='body', errors = ['fdlfjsf'])



# class TestCommentReplyViews(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email = 'morteza@gmail.com',
#             full_name = 'morteza N',
#             phone_number = '09389767293',
#             password = 'morteza info'
#         )
#         self.client = Client()
#         self.client.login(
#             email = 'morteza@gmail.com',
#             phone_number = '09389767293',
#             password = 'morteza info'
#         )
#     def test_login(self):
#         response = self.client.post(reverse('home:add_reply', args=['cloth', 1, 1]), data = {'user': self.user, })
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(reverse('home:product_detail', args=['cloth', 1]))
