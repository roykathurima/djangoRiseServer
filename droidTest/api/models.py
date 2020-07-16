from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class Product(models.Model):
	product_name 	= models.CharField(max_length=50)
	in_stock		= models.CharField(max_length=10)

	def __str__(self, *args, **kwargs):
		return self.product_name

class Unit(models.Model):
	product_id		= models.ForeignKey(Product, related_name='units', on_delete=models.CASCADE)
	unit_name		= models.CharField(max_length=20)
	pack_size		= models.IntegerField()
	price			= models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self, *args, **kwargs):
		return self.unit_name

class Orders(models.Model):
	customer_id		= models.IntegerField()
	date			= models.CharField(max_length=50)
	route_id		= models.IntegerField()
	total			= models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self, *args, **kwargs):
		return self.date

class OrderItem(models.Model):
	product_id		= models.IntegerField()
	qty				= models.IntegerField()
	unit_id			= models.IntegerField()
	subtotal		= models.DecimalField(max_digits=10, decimal_places=2)
	order_id		= models.ForeignKey(Orders, related_name='order_items', on_delete=models.CASCADE)
	
	def __str__(self, *args, **kwargs):
		return str(self.order_id)

# This is just a test model. Please do not do this in production...
class UserDetails(models.Model):
	username 		= models.CharField(max_length=20)
	password		= models.CharField(max_length=30)

	def __str__(self, *args, **kwargs):
		return self.username

class Route(models.Model):
	route_name		= models.CharField(max_length=40)
	sales_person	= models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self, *args, **kwargs):
		return self.route_name

class Customer(models.Model):
	customer_name	= models.CharField(max_length=40)
	phone_number	= models.CharField(max_length=20)
	route_id		= models.ForeignKey(Route, related_name='customers', on_delete=models.CASCADE)

	def __str__(self, *args, **kwargs):
		return self.customer_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)