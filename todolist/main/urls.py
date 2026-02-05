from django.urls import path
from .views.home import home as home_view
from .views.users import users_list, login as login_view, registration, logout as logout_view
from .views.employees import employees_list, employees_create, employees_edit, employees_delete, employees_bulk_delete
from .views.customers import customers_list, customers_create, customers_edit, customers_delete, customers_bulk_delete, customers_with_totals
from .views.products import products_list, products_create, products_edit, products_delete, products_bulk_delete
from .views.suppliers import suppliers_list, suppliers_create, suppliers_edit, suppliers_delete, suppliers_bulk_delete
from .views.categories import categories_list, categories_create, categories_edit, categories_delete, categories_bulk_delete
from .views.shippers import shippers_list, shippers_create, shippers_edit, shippers_delete, shippers_bulk_delete
from .views.orders import orders_list, orders_create, orders_edit, orders_delete, orders_bulk_delete
from .views.order_details import order_details_list, order_details_create, order_details_edit, order_details_delete, order_details_bulk_delete

urlpatterns = [
    path('', home_view, name='home'),
    # Users
    path('users/', users_list, name='users'),
    path('login/', login_view, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', logout_view, name='logout'),
    
    # Employees
    path('api/employees/', employees_list, name='employees_list'),
    path('api/employees/create/', employees_create, name='employees_create'),
    path('api/employees/edit/', employees_edit, name='employees_edit'),
    path('api/employees/delete/', employees_delete, name='employees_delete'),
    path('api/employees/bulk-delete/', employees_bulk_delete, name='employees_bulk_delete'),
    # Customers
    path('api/customers/', customers_list, name='customers'),
    path('api/customers/with-totals/', customers_with_totals, name='customers_with_totals'),
    path('api/customers/create/', customers_create, name='customers_create'),
    path('api/customers/edit/', customers_edit, name='customers_edit'),
    path('api/customers/delete/', customers_delete, name='customers_delete'),
    path('api/customers/bulk-delete/', customers_bulk_delete, name='customers_bulk_delete'),
    
    # Products
    path('api/products/', products_list, name='products'),
    path('api/products/create/', products_create, name='products_create'),
    path('api/products/edit/', products_edit, name='products_edit'),
    path('api/products/delete/', products_delete, name='products_delete'),
    path('api/products/bulk-delete/', products_bulk_delete, name='products_bulk_delete'),
    
    # Suppliers
    path('api/suppliers/', suppliers_list, name='suppliers'),
    path('api/suppliers/create/', suppliers_create, name='suppliers_create'),
    path('api/suppliers/edit/', suppliers_edit, name='suppliers_edit'),
    path('api/suppliers/delete/', suppliers_delete, name='suppliers_delete'),
    path('api/suppliers/bulk-delete/', suppliers_bulk_delete, name='suppliers_bulk_delete'),
    
    # Orders
    path('api/orders/', orders_list, name='orders'),
    path('api/orders/create/', orders_create, name='orders_create'),
    path('api/orders/edit/', orders_edit, name='orders_edit'),
    path('api/orders/delete/', orders_delete, name='orders_delete'),
    path('api/orders/bulk-delete/', orders_bulk_delete, name='orders_bulk_delete'),

    
    # Order Details
    path('api/orderdetails/', order_details_list, name='orderdetails'),
    path('api/orderdetails/create/', order_details_create, name='orderdetails_create'),
    path('api/orderdetails/edit/', order_details_edit, name='orderdetails_edit'),
    path('api/orderdetails/delete/', order_details_delete, name='orderdetails_delete'),
    path('api/orderdetails/bulk-delete/', order_details_bulk_delete, name='orderdetails_bulk_delete'),
    
    # Categories
    path('api/categories/', categories_list, name='categories'),
    path('api/categories/create/', categories_create, name='categories_create'),
    path('api/categories/edit/', categories_edit, name='categories_edit'),
    path('api/categories/delete/', categories_delete, name='categories_delete'),
    path('api/categories/bulk-delete/', categories_bulk_delete, name='categories_bulk_delete'),
    
    # Shippers
    path('api/shippers/', shippers_list, name='shippers'),
    path('api/shippers/create/', shippers_create, name='shippers_create'),
    path('api/shippers/edit/', shippers_edit, name='shippers_edit'),
    path('api/shippers/delete/', shippers_delete, name='shippers_delete'),
    path('api/shippers/bulk-delete/', shippers_bulk_delete, name='shippers_bulk_delete'),
]
