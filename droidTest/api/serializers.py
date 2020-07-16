from rest_framework import serializers

from .models import Product, Unit, Orders, OrderItem, UserDetails, Route, Customer


class CustomerSerialzer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
	customers = CustomerSerialzer(Customer.objects.all(), many=True)
	class Meta:
		model = Route
		fields = ['id', 'route_name', 'customers']

class UserDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserDetails
		fields = '__all__'
		
class UnitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Unit
		fields = '__all__'

class ProductSerliazer(serializers.ModelSerializer):
	units = UnitSerializer(Unit.objects.all(), many=True)
	class Meta:
		model = Product
		fields = ['id', 'product_name', 'in_stock', 'units']


class OrderItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderItem
		fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
	order_items = OrderItemSerializer(many=True)
	class Meta:
		model = Orders
		fields = ['id', 'customer_id', 'date', 'route_id', 'total', 'order_items']

	def create(self, validated_data):
		# Iterate through the list
		print("The create in the seializer")
		for data in validated_data:
			order_items_data = data.pop('order_items')
			orders = Orders.objects.create(**data)
			for order_items_dt in order_items_data:
				OrderItem.objects.create(order_id=orders, **order_items_dt)
			return orders





