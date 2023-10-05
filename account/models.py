from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, email,first_name,last_name,phone_number, password=None):
		if not email:
			raise ValueError('Users must have an email address')


		user = self.model(
			email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
			phone_number=phone_number,
		)
		user.set_password(password)
		user.is_admin = False
		user.is_staff = False
		user.save(using=self._db)
		return user

	def create_superuser(self, email,first_name,last_name,phone_number,  password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
            first_name=first_name,
            last_name=last_name,
			phone_number=phone_number,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user




class User(AbstractBaseUser):
	image=models.ImageField(upload_to='Images/profile')
	first_name=models.CharField(max_length=50,default='')
	last_name=models.CharField(max_length=50,default='')
	phone_number=models.CharField(max_length=50,default='')
	email=models.EmailField(unique=True, max_length=225)
	password=models.CharField(max_length=258,default='')
	profit=models.IntegerField(default=0)
	loss=models.IntegerField(default=0)
	active=models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff= models.BooleanField(default=False)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name','last_name','phone_number']

	objects = MyAccountManager()

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True




class Stock(models.Model):
	Product=models.CharField(max_length=50,default='')
	product_detials=models.CharField(max_length=250,default='')
	qnt=models.IntegerField(default=0)
	order_date=models.DateTimeField(auto_created=True)
	amnt=models.IntegerField(default=0)
	is_sold=models.BooleanField(default=False)

class Order_placed(models.Model):
	Product=models.CharField(max_length=50,default='')
	Order_by=models.CharField(max_length=50,default='')
	order_date=models.DateTimeField(auto_created=True)
	amnt=models.IntegerField(default=0)
	order_status=models.CharField(max_length=40, default='progress') #progress, on_the_way, done
	

