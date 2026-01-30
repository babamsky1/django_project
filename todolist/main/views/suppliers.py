from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Suppliers
from ..serializers import SuppliersSerializer, SuppliersCreateSerializer, SuppliersEditSerializer


@api_view(['GET'])
def suppliers_list(request):
    suppliers = Suppliers.objects.all()
    serializer = SuppliersSerializer(suppliers, many=True)

    return Response({
        "result": "success",
        "data": serializer.data,
        "message": "OK"
    }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def suppliers_create(request):
    if request.method == 'GET':
        # Return empty form structure or template info
        return Response({
            "result": "success",
            "data": serializer.data,
            "message": "OK"
        }, status=status.HTTP_200_OK)
    
    # POST method - create employee
    print(f"Request data: {request.data}")  # Debug line
    serializer = SuppliersCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            supplier = serializer.save()
            print(f"Supplier created: {supplier}")  # Debug line
            return Response({
                "result": "success",
                "data": serializer.data,
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
def suppliers_edit(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        supplier = Suppliers.objects.get(SupplierId=id)
        original_name = supplier.SupplierName
        serializer = SuppliersEditSerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "result": "success",
                "data": serializer.data,
                "previous_supplier_name": original_name,
                "message": "OK"
            }, status=status.HTTP_200_OK)
        return Response({
            "result": "error",
            "data": serializer.errors,
            "message": "Bad Request"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Suppliers.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Supplier not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def suppliers_delete(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        supplier = Suppliers.objects.get(SupplierId=id)
        supplier_name = supplier.SupplierName
        supplier.delete()
        return Response({
            "result": "success",
            "data": {"id": id, "deleted": True, "supplier_name": supplier_name},
            "message": "Supplier deleted successfully"
        }, status=status.HTTP_200_OK)
    except Suppliers.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Supplier not found"
        }, status=status.HTTP_404_NOT_FOUND)
