from rest_framework import serializers
from .models import Employees, Customers, Suppliers, Categories, Products, Shippers, Orders, Order_Details, User
from django.contrib.auth.hashers import make_password

# =========Employees Serializers=========
class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'
        
class EmployeesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['FirstName', 'LastName', 'BirthDate', 'Photo', 'Notes']
        
class EmployeesEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['FirstName', 'LastName', 'BirthDate', 'Photo', 'Notes']
        
class EmployeesDeleteSerializer(serializers.ModelSerializer):
    EmployeeId = serializers.CharField(read_only=True)
    
    class Meta:
        model = Employees
        fields = ['EmployeeId', 'FirstName', 'LastName'] 

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

# =========Suppliers Serializers=========
class SuppliersSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='SupplierName')
    contactName = serializers.CharField(source='ContactName')
    address = serializers.SerializerMethodField()
    
    class Meta:
        model = Suppliers
        fields = ['SupplierId', 'companyName', 'contactName', 'address']
    
    def get_address(self, obj):
        return {
            'street': obj.Address,
            'city': obj.City,
            'postalCode': obj.PostalCode,
            'country': obj.Country,
            'phone': obj.Phone
        }
        
class SuppliersCreateSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(write_only=True, required=False)
    contactName = serializers.CharField(write_only=True, required=False)
    address = serializers.DictField(write_only=True, required=False)
    
    class Meta:
        model = Suppliers
        fields = ['SupplierId', 'SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone', 'companyName', 'contactName', 'address']
        extra_kwargs = {
            'SupplierName': {'required': False},
            'ContactName': {'required': False},
            'Address': {'required': False},
            'City': {'required': False},
            'PostalCode': {'required': False},
            'Country': {'required': False},
            'Phone': {'required': False},
        }
    
    def validate(self, data):
        # Handle nested field names
        if 'companyName' in data:
            data['SupplierName'] = data.pop('companyName')
        if 'contactName' in data:
            data['ContactName'] = data.pop('contactName')
        
        # Handle nested address
        address_data = data.pop('address', {})
        if address_data:
            data['Address'] = address_data.get('street', data.get('Address', ''))
            data['City'] = address_data.get('city', data.get('City', ''))
            data['PostalCode'] = address_data.get('postalCode', data.get('PostalCode', ''))
            data['Country'] = address_data.get('country', data.get('Country', ''))
            data['Phone'] = address_data.get('phone', data.get('Phone', ''))
        
        # Validate required fields after transformation
        required_fields = ['SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: 'This field is required.'})
        
        return data
        
class SuppliersEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Suppliers
        fields = ['SupplierId', 'SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone']
        
class SuppliersDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Suppliers
        fields = ['SupplierId', 'SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone'] 
        
# =========Categories Serializers=========

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['CategoryId', 'CategoryName']
        
class CategoriesCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = ['CategoryId', 'CategoryName']
        
class CategoriesEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = ['CategoryId', 'CategoryName']
        
class CategoriesDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = ['CategoryId', 'CategoryName'] 
        

# =========Products Serializers=========
    
class ProductsSerializer(serializers.ModelSerializer):
    supplier = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    
    class Meta:
        model = Products
        fields = [
            'ProductId', 'ProductName', 'supplier', 'category', 
            'Price'
        ]
    
    def get_supplier(self, obj):
        return {
            'SupplierId': obj.Supplier.SupplierId,
            'companyName': obj.Supplier.SupplierName
        }
    
    def get_category(self, obj):
        return {
            'CategoryId': obj.Category.CategoryId,
            'CategoryName': obj.Category.CategoryName
        }
        
class ProductsCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = ['ProductId', 'ProductName', 'Supplier', 'Category', 'Price']
        
class ProductsEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = ['ProductId', 'ProductName', 'Supplier', 'Category', 'Price']
        
class ProductsDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = ['ProductId', 'ProductName', 'Supplier', 'Category', 'Price'] 
        
# =========Shippers Serializers=========

class ShippersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shippers
        fields = ['ShipperId', 'CompanyName', 'Phone']
        
class ShippersCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shippers
        fields = ['ShipperId', 'CompanyName', 'Phone']
        
class ShippersEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shippers
        fields = ['ShipperId', 'CompanyName', 'Phone']
        
class ShippersDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shippers
        fields = ['ShipperId', 'CompanyName', 'Phone'] 

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
