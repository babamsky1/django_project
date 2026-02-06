from django.db import models
import uuid

class User(models.Model):
    UserId = models.AutoField(primary_key=True, db_column='employeeid')
    LastName = models.CharField(max_length=150, db_column='lastname')
    FirstName = models.CharField(max_length=150, db_column='firstname')
    BirthDate = models.DateField(auto_now_add=False, db_column='birthdate')
    Photo = models.ImageField(upload_to='photos/', blank=True, null=True, db_column='photo')
    Notes = models.TextField(blank=True, db_column='notes')
    Email = models.EmailField(unique=True, db_column='email')
    Password = models.CharField(max_length=128, db_column='password')
    
    class Meta:
        db_table = "users"
        managed = False
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"User {self.FirstName} {self.LastName}"
    
class Employees(models.Model):
    EmployeeId = models.AutoField(primary_key=True, db_column='employeeid')
    FirstName = models.CharField(max_length=200, db_column='firstname')
    LastName = models.CharField(max_length=200, db_column='lastname')
    BirthDate = models.DateField(auto_now_add=False, db_column='birthdate')
    Photo = models.ImageField(upload_to='photos/', blank=True, null=True, db_column='photo')
    Notes = models.TextField(blank=True, db_column='notes')

    class Meta:
        db_table = "employees"
        managed = False
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"

class Customers(models.Model):
    CustomerId = models.AutoField(primary_key=True, db_column='customerid')
    CustomerName = models.CharField(max_length=200, db_column='customername')
    ContactName = models.CharField(max_length=200, db_column='contactname')
    City = models.CharField(max_length=200, db_column='city')
    Address = models.CharField(max_length=200, db_column='address')
    PostalCode = models.CharField(max_length=200, db_column='postalcode')
    Country = models.CharField(max_length=200, db_column='country')

    class Meta:
        db_table = "customers"
        managed = False
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.CustomerName

class Suppliers(models.Model):
    SupplierId = models.AutoField(primary_key=True, db_column='supplierid')
    SupplierName = models.CharField(max_length=200, db_column='suppliername')
    ContactName = models.CharField(max_length=200, db_column='contactname')
    Address = models.CharField(max_length=200, db_column='address')
    City = models.CharField(max_length=200, db_column='city')
    PostalCode = models.CharField(max_length=200, db_column='postalcode')
    Country = models.CharField(max_length=200, db_column='country')
    Phone = models.CharField(max_length=200, db_column='phone')
    
    class Meta:
        db_table = "suppliers"
        managed = False
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.SupplierName

class Categories(models.Model):
    CategoryId = models.AutoField(primary_key=True, db_column='categoryid')
    CategoryName = models.CharField(max_length=200, db_column='categoryname')
    Description = models.TextField(max_length=200, blank=True, null=True, db_column='description')
    
    class Meta:
        db_table = "categories"
        managed = False
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.CategoryName
    

class Products(models.Model):
    ProductId = models.AutoField(primary_key=True, db_column='productid')
    ProductName = models.CharField(max_length=200, db_column='productname')
    Supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, db_column='supplierid')
    Category = models.ForeignKey(Categories, on_delete=models.CASCADE, db_column='categoryid')
    Price = models.DecimalField(max_digits=10, decimal_places=2, db_column='price')

    class Meta:
        db_table = "products"
        managed = False
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.ProductName
    

class Shippers(models.Model):
    ShipperId = models.AutoField(primary_key=True, db_column='ShipperID')
    ShipperName = models.CharField(max_length=200, db_column='ShipperName')
    Phone = models.CharField(max_length=200, db_column='Phone')

    class Meta:
        db_table = "shippers"
        managed = False
        verbose_name = "Shipper"
        verbose_name_plural = "Shippers"

    def __str__(self):
        return self.ShipperName
    

class Order_Details(models.Model):
    OrderDetailId = models.AutoField(primary_key=True, db_column='orderdetailid')
    Product = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='productid')
    Quantity = models.IntegerField(default=1, db_column='quantity')
    Order = models.ForeignKey('Orders', on_delete=models.CASCADE, db_column='orderid')
    
    class Meta:
        db_table = "order_details"
        managed = False
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"

    def __str__(self):
        return f"{self.Product.ProductName} - {self.Quantity}"
    
    
class Orders(models.Model):
    OrderId = models.AutoField(primary_key=True, db_column='orderid')
    Customer = models.ForeignKey(Customers, on_delete=models.CASCADE, db_column='customerid')
    Employee = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='employeeid')
    OrderDate = models.DateField(db_column='orderdate')
    Shipper = models.ForeignKey(Shippers, on_delete=models.CASCADE, db_column='shipperid')
    
    class Meta:
        db_table = "orders"
        managed = False
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.OrderId} - {self.Customer.CustomerName}"
    
