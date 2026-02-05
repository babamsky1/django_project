from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Order_Details
from ..serializers import OrderDetailsSerializer, OrderDetailsCreateSerializer, OrderDetailsEditSerializer


@api_view(['GET'])
def order_details_list(request):
    order_details = Order_Details.objects.all()
    serializer = OrderDetailsSerializer(order_details, many=True)

    return Response({
        "result": "success",
        "data": serializer.data,
        "message": "OK"
    }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def order_details_create(request):
    if request.method == 'GET':
        # Return empty form structure or template info
        return Response({
            "result": "success",
            "data": serializer.data,
            "message": "OK"
        }, status=status.HTTP_200_OK)
    
    # POST method - create order detail
    print(f"Request data: {request.data}")  # Debug line
    serializer = OrderDetailsCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            order_detail = serializer.save()
            print(f"Order detail created: {order_detail}")  # Debug line
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
def order_details_edit(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        order_detail = Order_Details.objects.get(OrderDetailId=id)
        original_order_detail_id = order_detail.OrderDetailId
        serializer = OrderDetailsEditSerializer(order_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "result": "success",
                "data": serializer.data,
                "previous_order_detail_id": original_order_detail_id,
                "message": "OK"
            }, status=status.HTTP_200_OK)
        return Response({
            "result": "error",
            "data": serializer.errors,
            "message": "Bad Request"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Order_Details.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Order detail not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def order_details_delete(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        order_detail = Order_Details.objects.get(OrderDetailId=id)
        order_detail_id = order_detail.OrderDetailId
        order_detail.delete()
        return Response({
            "result": "success",
            "data": {"id": id, "deleted": True, "order_detail_id": order_detail_id},
            "message": "Order detail deleted successfully"
        }, status=status.HTTP_200_OK)
    except Order_Details.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Order detail not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def order_details_bulk_delete(request):
    try:
        ids = request.data.get('ids')
        if not ids:
            return Response({
                "result": "error",
                "message": "IDs are required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        order_details = Order_Details.objects.filter(OrderDetailId__in=ids)
        order_details_count = order_details.count()
        order_details.delete()
        return Response({
            "result": "success",
            "data": {"ids": ids, "deleted": True, "order_details_count": order_details_count},
            "message": "Order details deleted successfully"
        }, status=status.HTTP_200_OK)
    except Order_Details.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Order details not found"
        }, status=status.HTTP_404_NOT_FOUND)
