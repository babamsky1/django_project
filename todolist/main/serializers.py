from rest_framework import serializers
from .models import Employees, Customers, Suppliers, Categories, Products, Shippers, Orders, Order_Details, User
from django.contrib.auth.hashers import make_password

# =========Employees Serializers=========
class EmployeesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employees
        fields = ['EmployeeId', 'FirstName', 'LastName', 'BirthDate', 'Photo', 'Notes']
        
class EmployeesCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employees
        fields = ['EmployeeId', 'FirstName', 'LastName', 'BirthDate', 'Photo', 'Notes']
        
class EmployeesEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employees
        fields = ['EmployeeId', 'FirstName', 'LastName', 'BirthDate', 'Photo', 'Notes']
        
class EmployeesDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employees
        fields = ['EmployeeId', 'FirstName', 'LastName'] 
        
class EmployeesBulkDeleteSerializer(serializers.ModelSerializer):
    EmployeeId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Employees
        fields = ['EmployeeId'] 

# =========Customers Serializers=========
class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['CustomerId', 'CustomerName', 'ContactName', 'City', 'Address', 'PostalCode', 'Country']

        
class CustomersCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Customers
        fields = ['CustomerId', 'CustomerName', 'ContactName', 'City', 'Address', 'PostalCode', 'Country']
        
class CustomersEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customers
        fields = ['CustomerId', 'CustomerName', 'ContactName', 'City', 'Address', 'PostalCode', 'Country']
        
class CustomersDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customers
        fields = ['CustomerId', 'CustomerName', 'ContactName', 'City', 'Address', 'PostalCode', 'Country'] 
        
class CustomersBulkDeleteSerializer(serializers.ModelSerializer):
    CustomerId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Customers
        fields = ['CustomerId'] 

# Suppliers Serializers
class SuppliersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suppliers
        fields = ['SupplierId', 'SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone']


# Suppliers Create Serializers
class SuppliersCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suppliers
        fields = ['SupplierId', 'SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone']
        extra_kwargs = {field: {'required': False} for field in ['ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone']}


# Suppliers Edit Serializers
class SuppliersEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ['SupplierId', 'SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone']


# Suppliers Delete Serializers
class SuppliersDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ['SupplierId']
        
class SuppliersBulkDeleteSerializer(serializers.ModelSerializer):
    SupplierId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Suppliers
        fields = ['SupplierId'] 
        
        
# =========Categories Serializers=========

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['CategoryId', 'CategoryName', 'Description']
        
class CategoriesCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = ['CategoryId', 'CategoryName', 'Description']
        
class CategoriesEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = ['CategoryId', 'CategoryName', 'Description']
        
class CategoriesDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = ['CategoryId', 'CategoryName', 'Description'] 
        
class CategoriesBulkDeleteSerializer(serializers.ModelSerializer):
    CategoryId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Categories
        fields = ['CategoryId', 'CategoryName', 'Description'] 
        

# =========Products Serializers=========
    
class ProductsSerializer(serializers.ModelSerializer):
    Supplier = serializers.SerializerMethodField()
    Category = serializers.SerializerMethodField()
    
    class Meta:
        model = Products
        fields = [
            'ProductId', 'ProductName', 'Supplier', 'Category', 
            'Price'
        ]
    
    def get_Supplier(self, obj):
        if hasattr(obj, 'Supplier') and obj.Supplier:
            return {
                'SupplierId': obj.Supplier.SupplierId,
                'SupplierName': obj.Supplier.SupplierName
            }
        return None
    
    def get_Category(self, obj):
        if hasattr(obj, 'Category') and obj.Category:
            return {
                'CategoryId': obj.Category.CategoryId,
                'CategoryName': obj.Category.CategoryName,
                'Description': obj.Category.Description
            }
        return None
        
class ProductsCreateSerializer(serializers.ModelSerializer):
    Supplier = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all())
    Category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())
    
    class Meta:
        model = Products
        fields = ['ProductId', 'ProductName', 'Supplier', 'Category', 'Price']
        
class ProductsEditSerializer(serializers.ModelSerializer):
    Supplier = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all(), required=False)
    Category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), required=False)
    
    class Meta:
        model = Products
        fields = ['ProductId', 'ProductName', 'Supplier', 'Category', 'Price']
    
    def validate_Supplier(self, value):
        if value is None:
            supplier_data = self.initial_data.get('Supplier')
            if isinstance(supplier_data, dict):
                try:
                    return Suppliers.objects.get(SupplierId=supplier_data['SupplierId'])
                except Suppliers.DoesNotExist:
                    raise serializers.ValidationError("Supplier not found")
            elif supplier_data:
                try:
                    return Suppliers.objects.get(SupplierId=supplier_data)
                except Suppliers.DoesNotExist:
                    raise serializers.ValidationError("Supplier not found")
        return value
    
    def validate_Category(self, value):
        if value is None:
            category_data = self.initial_data.get('Category')
            if isinstance(category_data, dict):
                try:
                    return Categories.objects.get(CategoryId=category_data['CategoryId'])
                except Categories.DoesNotExist:
                    raise serializers.ValidationError("Category not found")
            elif category_data:
                try:
                    return Categories.objects.get(CategoryId=category_data)
                except Categories.DoesNotExist:
                    raise serializers.ValidationError("Category not found")
        return value
        
class ProductsDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = ['ProductId', 'ProductName', 'Supplier', 'Category', 'Price'] 
        
class ProductsBulkDeleteSerializer(serializers.ModelSerializer):
    ProductId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Products
        fields = ['ProductId', 'ProductName', 'Supplier', 'Category', 'Price'] 
        
# =========Shippers Serializers=========

class ShippersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shippers
        fields = ['ShipperId', 'ShipperName', 'Phone']
        
class ShippersCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shippers
        fields = ['ShipperId', 'ShipperName', 'Phone']
        
class ShippersEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shippers
        fields = ['ShipperId', 'ShipperName', 'Phone']
        
class ShippersDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shippers
        fields = ['ShipperId', 'ShipperName', 'Phone'] 
        
class ShippersBulkDeleteSerializer(serializers.ModelSerializer):
    ShipperId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Shippers
        fields = ['ShipperId', 'ShipperName', 'Phone'] 

# =========Orders Serializers=========

class OrdersSerializer(serializers.ModelSerializer):
    OrderId = serializers.CharField(read_only=True)
    class Meta:
        model = Orders
        fields = ['OrderId', 'Customer', 'Employee', 'OrderDate', 'Shipper']
        
class OrdersCreateSerializer(serializers.ModelSerializer):
    OrderId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Orders
        fields = ['OrderId', 'Customer', 'Employee', 'OrderDate', 'Shipper']
        
class OrdersEditSerializer(serializers.ModelSerializer):
    OrderId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Orders
        fields = ['OrderId', 'Customer', 'Employee', 'OrderDate', 'Shipper']
        
class OrdersDeleteSerializer(serializers.ModelSerializer):
    OrderId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Orders
        fields = ['OrderId', 'Customer', 'Employee', 'OrderDate', 'Shipper'] 

class OrdersBulkDeleteSerializer(serializers.ModelSerializer):
    OrderId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Orders
        fields = ['OrderId', 'Customer', 'Employee', 'OrderDate', 'Shipper'] 

# =========Order Details Serializers=========

class OrderDetailsSerializer(serializers.ModelSerializer):
    OrderDetailId = serializers.CharField(read_only=True)
    class Meta:
        model = Order_Details
        fields = ['OrderDetailId', 'Order', 'Product', 'Quantity']
        
class OrderDetailsCreateSerializer(serializers.ModelSerializer):
    OrderDetailId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order_Details
        fields = ['OrderDetailId', 'Order', 'Product', 'Quantity']
        
class OrderDetailsEditSerializer(serializers.ModelSerializer):
    OrderDetailId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order_Details
        fields = ['OrderDetailId', 'Order', 'Product', 'Quantity']
        
class OrderDetailsDeleteSerializer(serializers.ModelSerializer):
    OrderDetailId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order_Details
        fields = ['OrderDetailId', 'Order', 'Product', 'Quantity'] 
        
class OrderDetailsBulkDeleteSerializer(serializers.ModelSerializer):
    OrderDetailId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order_Details
        fields = ['OrderDetailId', 'Order', 'Product', 'Quantity'] 
        
# =========User Serializers=========

class UserSerializer(serializers.ModelSerializer):
    UserId = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password before saving
        if 'Password' in validated_data:
            validated_data['Password'] = make_password(validated_data['Password'])
        return super().create(validated_data)
    
class UserCreateSerializer(serializers.ModelSerializer):
    UserId = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['UserId', 'FirstName', 'Email', 'Password']
        
class UserEditSerializer(serializers.ModelSerializer):
    UserId = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['UserId', 'FirstName', 'Email']
        
class UserDeleteSerializer(serializers.ModelSerializer):
    UserId = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['UserId', 'FirstName', 'Email']
