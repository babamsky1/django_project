from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Customers
from ..serializers import CustomersSerializer, CustomersCreateSerializer, CustomersEditSerializer


@api_view(['GET', 'POST'])
def customers_list(request):
    # Standard customers list
    customers = Customers.objects.all()
    serializer = CustomersSerializer(customers, many=True)

    return Response({
        "result": "success",
        "data": serializer.data,
        "message": "OK"
    }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def customers_create(request):
    if request.method == 'GET':
        # Return empty form structure or template info
        return Response({
            "result": "success",
            "data": serializer.data,
            "message": "OK"
        }, status=status.HTTP_200_OK)
    
    # POST method - create customer
    print(f"Request data: {request.data}")  # Debug line
    serializer = CustomersCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            customer = serializer.save()
            print(f"Customer created: {customer}")  # Debug line
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
def customers_edit(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        customer = Customers.objects.get(CustomerId=id)
        original_name = customer.CustomerName
        serializer = CustomersEditSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "result": "success",
                "data": serializer.data,
                "previous_customer_name": original_name,
                "message": "OK"
            }, status=status.HTTP_200_OK)
        return Response({
            "result": "error",
            "data": serializer.errors,
            "message": "Bad Request"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Customers.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Customer not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def customers_delete(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        customer = Customers.objects.get(CustomerId=id)
        customer_name = customer.CustomerName
        customer.delete()
        return Response({
            "result": "success",
            "data": {"id": id, "deleted": True, "customer_name": customer_name},
            "message": "Customer deleted successfully"
        }, status=status.HTTP_200_OK)
    except Customers.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Customer not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def customers_bulk_delete(request):
    try:
        ids = request.data.get('ids')
        if not ids:
            return Response({
                "result": "error",
                "message": "IDs are required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        customers = Customers.objects.filter(CustomerId__in=ids)
        customers_count = customers.count()
        customers.delete()
        return Response({
            "result": "success",
            "data": {"ids": ids, "deleted": True, "customers_count": customers_count},
            "message": "Customers deleted successfully"
        }, status=status.HTTP_200_OK)
    except Customers.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Customers not found"
        }, status=status.HTTP_404_NOT_FOUND)
