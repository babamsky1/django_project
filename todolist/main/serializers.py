from rest_framework import serializers
from .models import Employees, Customers, Suppliers, Categories, Products, Shippers, Orders, Order_Details, User
from django.contrib.auth.hashers import make_password
from django.db.models import Sum, F

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
    total_spent = serializers.SerializerMethodField()
    
    class Meta:
        model = Customers
        fields = ['CustomerId', 'CustomerName', 'ContactName', 'City', 'Address', 'PostalCode', 'Country', 'total_spent']
    
    def get_total_spent(self, obj):
        # Calculate total spent for this customer
        total = Order_Details.objects.filter(
            Order__Customer=obj
        ).aggregate(
            total=Sum(F('Quantity') * F('Product__Price'))
        )['total'] or 0
        return float(total) if total else 0.0

        
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
    CustomerName = serializers.SerializerMethodField()
    EmployeeName = serializers.SerializerMethodField()
    ShipperName = serializers.SerializerMethodField()
    
    class Meta:
        model = Orders
        fields = ['OrderId', 'Customer', 'Employee', 'OrderDate', 'Shipper', 'CustomerName', 'EmployeeName', 'ShipperName']
    
    def get_CustomerName(self, obj):
        if hasattr(obj, 'Customer') and obj.Customer:
            return obj.Customer.CustomerName
        return None
    
    def get_EmployeeName(self, obj):
        if hasattr(obj, 'Employee') and obj.Employee:
            return f"{obj.Employee.FirstName} {obj.Employee.LastName}"
        return None
    
    def get_ShipperName(self, obj):
        if hasattr(obj, 'Shipper') and obj.Shipper:
            return obj.Shipper.ShipperName
        return None
        
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
    
    # Return frontend-friendly field names
    productId = serializers.IntegerField(source='Product', read_only=True)
    orderId = serializers.IntegerField(source='Order', read_only=True)
    quantity = serializers.IntegerField(source='Quantity', read_only=True)
    
    # Keep backend fields for compatibility but mark read-only
    Product = serializers.IntegerField(read_only=True)
    Order = serializers.IntegerField(read_only=True)
    Quantity = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Order_Details
        fields = ['OrderDetailId', 'Order', 'Product', 'Quantity', 'productId', 'orderId', 'quantity']
        
class OrderDetailsCreateSerializer(serializers.ModelSerializer):
    OrderDetailId = serializers.CharField(read_only=True)
    
    # Accept frontend field names and map to backend fields
    productId = serializers.IntegerField(write_only=True, required=False)
    orderId = serializers.IntegerField(write_only=True, required=False)
    quantity = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Order_Details
        fields = ['OrderDetailId', 'Order', 'Product', 'Quantity', 'productId', 'orderId', 'quantity']
        extra_kwargs = {
            'Order': {'write_only': True},
            'Product': {'write_only': True},
            'Quantity': {'write_only': True},
        }
    
    def validate(self, attrs):
        # Map frontend fields to backend fields
        if 'productId' in attrs:
            attrs['Product'] = attrs.pop('productId')
        if 'orderId' in attrs:
            attrs['Order'] = attrs.pop('orderId')
        if 'quantity' in attrs:
            attrs['Quantity'] = attrs.pop('quantity')
        return attrs
        
class OrderDetailsEditSerializer(serializers.ModelSerializer):
    OrderDetailId = serializers.CharField(read_only=True)
    
    # Accept frontend field names and map to backend fields
    productId = serializers.IntegerField(write_only=True, required=False)
    orderId = serializers.IntegerField(write_only=True, required=False)
    quantity = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Order_Details
        fields = ['OrderDetailId', 'Order', 'Product', 'Quantity', 'productId', 'orderId', 'quantity']
        extra_kwargs = {
            'Order': {'write_only': True},
            'Product': {'write_only': True},
            'Quantity': {'write_only': True},
        }
    
    def validate(self, attrs):
        # Map frontend fields to backend fields
        if 'productId' in attrs:
            attrs['Product'] = attrs.pop('productId')
        if 'orderId' in attrs:
            attrs['Order'] = attrs.pop('orderId')
        if 'quantity' in attrs:
            attrs['Quantity'] = attrs.pop('quantity')
        return attrs
        
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
