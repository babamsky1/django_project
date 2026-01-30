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
    
@api_view(['POST'])
def order_details_create(request):
    serializer = OrderDetailsCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "result": "success",
            "data": serializer.data,
            "message": "OK"
        }, status=status.HTTP_201_CREATED)
    return Response({
        "result": "error",
        "data": serializer.errors,
        "message": "Bad Request"
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
        original_name = f"Order Detail {order_detail.OrderDetailId}"
        serializer = OrderDetailsEditSerializer(order_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "result": "success",
                "data": serializer.data,
                "previous_order_detail_name": original_name,
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
            "message": "Order Detail not found"
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
        order_detail_name = f"Order Detail {order_detail.OrderDetailId}"
        order_detail.delete()
        return Response({
            "result": "success",
            "data": {"id": id, "deleted": True, "order_detail_name": order_detail_name},
            "message": "Order Detail deleted successfully"
        }, status=status.HTTP_200_OK)
    except Order_Details.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Order Detail not found"
        }, status=status.HTTP_404_NOT_FOUND)
