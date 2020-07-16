from django.urls import path
from .views import ProductsListView, OrdersApiView, UserListView, CustomerAndRouteView, CustomerCreateView, CustomerUpdateView

urlpatterns = [
	path('list', ProductsListView.as_view(), name='product_list'),
	path('post', OrdersApiView.as_view(), name='order_list'),
	path('login', UserListView.as_view(), name='api_login'),
	path('routecusts', CustomerAndRouteView.as_view(), name='routecusts'),
	path('create_customer', CustomerCreateView.as_view(), name='create_customer'),
	path('create_customer/<int:pk>', CustomerUpdateView.as_view(), name='customer_detail'),


]