from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from authentication.utils import generate_token
from django.test import Client

# Create your tests here.
class BaseTest(TestCase):
	def setUp(self):
		self.home_url=reverse('home')
		self.gamemaster_url=reverse('gamemaster_login')
		self.register_url=reverse('register')
		self.login_url=reverse('login')
		self.user={
			'username':'username',
			'email':'test@gmail.com',
			'password':'password',
			'password2':'password2'
		}

		self.user_short_password={
			'username':'username',
			'email':'test@gmail.com',
			'password':'sho',
			'password2':'sho'
		}

		self.user_invalid_email={
			'username':'username',
			'email':'test',
			'password':'university1',
			'password2':'university1'
		}

		self.user_unmatching_password={
			'username':'username',
			'email':'test',
			'password':'university1',
			'password2':'universe'
		}

		# Group setup
        group_name = "Gamemaster"
        self.group = Group(name=group_name)
        self.group.save()

		return super().setUp()

def RegisterTest(BaseTest):
	def test_can_view_page_correctly(self):
		response=self.client.get(self.register_url)
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'users/register.html')

	def test_can_register_user(self):
		respone=self.client.post(self.register_url.self.user,format='text/html')
		self.assertEqual(response.status_code,302)

	def test_cant_register_user_withshortpassword(self):
    	response=self.client.post(self.register_url,self.user_short_password,format='text/html')
    	self.assertEqual(response.status_code,400)

    def test_cant_register_with_invalid_email(self):
    	response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
    	self.assertEqual(response.status_code,400)

    def test_unmatching_password_cant_register(self):
    	response=response=self.client.post(self.register_url,self.user_unmatching_password,format='text/html')
    	self.assertEqual(response.status_code,400)

class LoginTest(BaseTest):
	def test_access_page(self):
		respone=self.client.get(self.login_url)
		self.assertEqual(response,status_code,200)
		self.assertTemplateUsed(response, 'users/login.html')

	def test_loginsucces(self):
		self.client.post(self.register_url, self.user, format='text/html')
		user=User.objects.filter(email=self.user['email']).first()
		user.is_active=True
		user.save()
		response=self.client.post(self.login_url,self.user,format='text/html')
		self.assertEqual(response.status_code,302)

	def test_cantlogin_no_username(self):
		response = self.client.post(self.login_url,{'password':'password', 'username':''}, format='text/html')
		self.assertEqual(response.status_code,302)

	def test_cantlogin_no_username(self):
		response = self.client.post(self.login_url,{'password':'', 'username':'Iestynlee'}, format='text/html')
		self.assertEqual(response.status_code,302)

class GameMasterLoginTest(BaseTest):
	def test_access_page(self):
		respone=self.client.get(self.gamemaster_url)
		self.assertEqual(response,status_code,200)
		self.assertTemplateUsed(response, 'users/gamemaster_login.html')

	def test_loginsucces(self):
		self.client.post(self.register_url, self.user, format='text/html')
		user=User.objects.filter(email=self.user['email']).first()
		user.is_active=True
		user.save()
		response=self.client.post(self.login_url,self.user,format='text/html')
		self.assertEqual(response.status_code,302)

	def test_cantlogin_no_username(self):
		response = self.client.post(self.login_url,{'password':'password', 'username':''}, format='text/html')
		self.assertEqual(response.status_code,302)

	def test_cantlogin_no_username(self):
		response = self.client.post(self.login_url,{'password':'', 'username':'Iestynlee'}, format='text/html')
		self.assertEqual(response.status_code,302)

class HomeTest(BaseTest):
	def test_access_page(self):
		respone=self.client.get(self.home_url)
		self.assertEqual(response,status_code,200)
		self.assertTemplateUsed(response, 'users/home.html')