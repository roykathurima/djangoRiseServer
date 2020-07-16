from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Product, Unit, Orders, OrderItem, Route, Customer
# import json
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerliazer, UnitSerializer, OrderItemSerializer, OrdersSerializer, UserDetailsSerializer, CustomerSerialzer, RouteSerializer


# 40ba18169d5b24f323e79fec93706082b7d6476d -> Roy
# cf58af79eea1d10911d68f399abcfd7d7c139311 -> Eric

# The customer endpoint must have both a get and a set... Lets do the get first
# on second thought, lets do the post in a seperate endpoint.
class CustomerAndRouteView(generics.GenericAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = RouteSerializer
	# queryset = Route.objects.all()
	# Override the get_queryset method to return the data that you want
	def get_queryset(self, request, *args, **kwargs):
		return Route.objects.filter(sales_person = request.user)

	def get(self, request, *args, **kwargs):
		print(request.user)
		serializer = RouteSerializer(self.get_queryset(request), many=True)
		return Response(serializer.data)

class CustomerCreateView(generics.CreateAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = CustomerSerialzer
	def post(self, request, *args, **kwargs):
		print(request.data)
		return self.create(request, *args, **kwargs)
	def create(self, request, *args, **kwargs):
		r_id = request.data.pop('route_id')
		name = request.data.pop('customer_name')
		number = request.data.pop('phone_number')
		route = Route.objects.get(id=r_id)
		Customer.objects.create(customer_name=name, phone_number=number, route_id=route)
		return Response({'code':0, 'Result': 'Successfully added the new Customer'})

class CustomerUpdateView(generics.RetrieveUpdateDestroyAPIView):
	# Initially it was just UpdateAPIView
	permission_classes = (IsAuthenticated,)
	serializer_class = CustomerSerialzer
	queryset = Customer.objects.all()
	# Remember that the route_id expects an instance of the route and not an id


# Not a very good idea of doing this but its https and its POST so whatevs
# Do the checks on the client side, so that I do not have to write excessive code
# na ikuwe sitatumia this server in production... would be a total waste
class UserListView(generics.GenericAPIView):
	serializer_class = UserDetailsSerializer
	def post(self, request, *args, **kwargs):
		print(request.data)
		u_name = request.data.pop('username')
		passwd = request.data.pop('password')
		user = authenticate(username=u_name, password=passwd)
		if(user is not None):
			tk = Token.objects.get(user=user)
			# just pass it the damn object and it'll serialize it on its own
			# token_response = json.dumps({'token': tk.key})
			return Response({'token': tk.key})
			# How about I create a token Model that will serialize this for me

class ProductsListView(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Product.objects.all()
	serializer_class = ProductSerliazer

	# the request.user contains the value of the currently authenticate user
	# def get(self, *args, **kwargs):
	# 	print(self.request.user)
	# The request.auth contains the value of the token
	# 	print(self.request.auth)

	# def get_queryset(self):
	# 	# This is where I specify the records I want returned.

	# 	return Product.objects.all()

class OrdersApiView(mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Orders.objects.all()
	serializer_class = OrdersSerializer

	def post(self, request, *args, **kwargs):
		print(request.body)
		return self.create(request, *args, **kwargs)

	def create(self, request):
		lst = []
		for dt in request.data:
			order_items_data = dt.pop('order_items')
			# print(dt)
			# print(dir(dt))
			# This is where you check if the order has a negative customer_id,
			# if it does, we need to store it in the database, retrieve the newly inserted id
			# the use it to create the order object.

			# Customer.objects.latest('id').id
			orders = Orders.objects.create(**dt)
			lst.append(dt.get('id'))
			# print(lst)
			# print("this is the 2nd dt --> is the item popped like in stack?")
			# print(dt)
			# print(order_items_data)
			for order_data in order_items_data:
				print(order_data)
				OrderItem.objects.create(order_id=orders, product_id=order_data['product_id'], qty=order_data['qty'], unit_id=order_data['unit_id'], subtotal=order_data['subtotal'])
		return Response(lst)
			
		# order_items_data = request.data.pop('order_items')
		# orders = Orders.objects.create(**data)
		# for order_items_dt in order_items_data:
		# 	OrderItem.objects.create(orders=orders, **order_items_dt)
		# return orders

	# def create(self, request):
	# 	# print(dir(validated_data))
	# 	print(request.data)
	# 	order_items_data = request.data[0].pop('order_items')
	# 	print("printing order items data....")
	# 	print(order_items_data)
	# 	orders = Orders.objects.create(**request.data[0])
	# 	OrderItem.objects.create(orders=orders, **order_items_data)
	# 	return orders
