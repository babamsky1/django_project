from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Shippers
from ..serializers import ShippersSerializer, ShippersCreateSerializer, ShippersEditSerializer


@api_view(['GET'])
def shippers_list(request):
    shippers = Shippers.objects.all()
    serializer = ShippersSerializer(shippers, many=True)

    return Response({
        "result": "success",
        "data": serializer.data,
        "message": "OK"
    }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def shippers_create(request):
    if request.method == 'GET':
        # Return empty form structure or template info
        return Response({
            "result": "success",
            "data": serializer.data,
            "message": "OK"
        }, status=status.HTTP_200_OK)
    
    # POST method - create employee
    print(f"Request data: {request.data}")  # Debug line
    serializer = ShippersCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            shipper = serializer.save()
            print(f"Shipper created: {shipper}")  # Debug line
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
def shippers_edit(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        shipper = Shippers.objects.get(ShipperId=id)
        original_name = shipper.CompanyName
        serializer = ShippersSerializer(shipper, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "result": "success",
                "data": serializer.data,
                "previous_company_name": original_name,
                "message": "OK"
            }, status=status.HTTP_200_OK)
        return Response({
            "result": "error",
            "data": serializer.errors,
            "message": "Bad Request"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Shippers.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Shipper not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def shippers_delete(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        shipper = Shippers.objects.get(ShipperId=id)
        company_name = shipper.CompanyName
        shipper.delete()
        return Response({
            "result": "success",
            "data": {"id": id, "deleted": True, "company_name": company_name},
            "message": "Shipper deleted successfully"
        }, status=status.HTTP_200_OK)
    except Shippers.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Shipper not found"
        }, status=status.HTTP_404_NOT_FOUND)
