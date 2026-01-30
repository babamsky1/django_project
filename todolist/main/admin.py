from django.contrib import admin
from .models import Employees, Customers, Suppliers, Categories, Products, Shippers, Orders, Order_Details, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.register(User)
admin.site.register(Employees)
admin.site.register(Customers)
admin.site.register(Suppliers)
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Shippers)
admin.site.register(Orders)
admin.site.register(Order_Details) 