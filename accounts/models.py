from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
	def create_user(self,email,password,username=None,**kwargs):
		if not email:
			raise ValueError('Phone Number must be set')

		user = self.model(email=email,**kwargs)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password,username=None, **kwargs):
		kwargs.setdefault('is_staff', True)
		kwargs.setdefault('is_superuser', True)
		kwargs.setdefault('is_active', True)
		user = self.create_user(email,password,username=None,**kwargs)
		user.is_admin = True
		user.save()
		return user

##User:
class CustomUser(AbstractUser):
	id 				= models.AutoField(primary_key=True)
	username 		= models.CharField(max_length=255,blank=True)
	name 			= models.CharField(blank=True,null=True,max_length=255)
	surname 		= models.CharField(blank=True,null=True,max_length=255)

	is_doctor 		= models.BooleanField(default=False)
	password 		= models.CharField(max_length=255)
	email 			= models.EmailField(max_length=254,unique=True)
	phone_number 	= models.IntegerField(blank=True,null=True)
	date_created	= models.DateField(auto_now=True,editable=False)

	is_active 		= models.BooleanField(default=True)
	is_admin 		= models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
		return str(self.email)
