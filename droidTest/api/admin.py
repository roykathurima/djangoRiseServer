from django.contrib import admin
from .models import Product, Unit, Orders, OrderItem, Route, Customer

admin.site.register(Product)
admin.site.register(Unit)
admin.site.register(OrderItem)
admin.site.register(Orders)
admin.site.register(Route)
admin.site.register(Customer)
