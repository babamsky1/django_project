from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products, Suppliers, Categories
from ..serializers import ProductsSerializer, ProductsCreateSerializer, ProductsEditSerializer, ProductsDeleteSerializer


@api_view(['GET'])
def products_list(request):
    products = Products.objects.all()
    serializer = ProductsSerializer(products, many=True)

    return Response({
        "result": "success",
        "data": serializer.data,
        "message": "OK"
    }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def products_create(request):
    if request.method == 'GET':
        # Return empty form structure or template info
        return Response({
            "result": "success",
            "data": {},
            "message": "OK"
        }, status=status.HTTP_200_OK)
    
    # POST method - create product
    print(f"Request data: {request.data}")  # Debug line
    serializer = ProductsCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            product = serializer.save()
            print(f"Product created: {product}")  # Debug line
            # Return full product data with relationships
            full_serializer = ProductsSerializer(product)
            return Response({
                "result": "success",
                "data": full_serializer.data,
                "message": "OK"
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Save error: {e}")  # Debug line
            return Response({
                "result": "error",
                "data": str(e),
                "message": "Database error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print(f"Validation errors: {serializer.errors}")  # Debug line
        return Response({
            "result": "error",
            "data": serializer.errors,
            "message": "Validation failed"
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def products_edit(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        product = Products.objects.get(ProductId=id)
        original_name = product.ProductName
        serializer = ProductsEditSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = ProductsSerializer(product)
            return Response({
                "result": "success",
                "data": response_serializer.data,
                "previous_product_name": original_name,
                "message": "OK"
            }, status=status.HTTP_200_OK)
        return Response({
            "result": "error",
            "data": serializer.errors,
            "message": "Bad Request"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Products.DoesNotExist:
        return Response({           
            "result": "error",
            "message": "Product not found"
        }, status=status.HTTP_404_NOT_FOUND)

        
@api_view(['DELETE'])
def products_delete(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        product = Products.objects.get(ProductId=id)
        product_name = product.ProductName
        product.delete()
        return Response({
            "result": "success",
            "data": {"id": id, "deleted": True, "product_name": product_name},
            "message": "Product deleted successfully"
        }, status=status.HTTP_200_OK)
    except Products.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Product not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def products_bulk_delete(request):
    try:
        ids = request.data.get('ids')
        if not ids:
            return Response({
                "result": "error",
                "message": "IDs are required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        products = Products.objects.filter(ProductId__in=ids)
        products_count = products.count()
        products.delete()
        return Response({
            "result": "success",
            "data": {"ids": ids, "deleted": True, "products_count": products_count},
            "message": "Products deleted successfully"
        }, status=status.HTTP_200_OK)
    except Products.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Products not found"
        }, status=status.HTTP_404_NOT_FOUND)
