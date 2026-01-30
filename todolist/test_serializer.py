import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todolist.settings')
django.setup()

from main.models import Products
from main.serializers import ProductsSerializer

product = Products.objects.first()
serializer = ProductsSerializer(product)
print("Serialized data:")
print(serializer.data)
