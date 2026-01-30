import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todolist.settings')
django.setup()

from main.models import Products, Suppliers, Categories

print(f'Products count: {Products.objects.count()}')
print(f'Suppliers count: {Suppliers.objects.count()}')
print(f'Categories count: {Categories.objects.count()}')

if Products.objects.exists():
    p = Products.objects.first()
    print(f'First product: {p}')
    print(f'Product ID: {p.ProductId}')
    print(f'Product Name: {p.ProductName}')
    print(f'Supplier ID: {p.Supplier.SupplierId if p.Supplier else None}')
    print(f'Supplier Name: {p.Supplier.SupplierName if p.Supplier else "None"}')
    print(f'Category ID: {p.Category.CategoryId if p.Category else None}')
    print(f'Category Name: {p.Category.CategoryName if p.Category else "None"}')
else:
    print("No products found")
