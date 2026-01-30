from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Orders
from ..serializers import OrdersSerializer, OrdersCreateSerializer, OrdersEditSerializer


@api_view(['GET'])
def orders_list(request):
    orders = Orders.objects.all()
    serializer = OrdersSerializer(orders, many=True)

    return Response({
        "result": "success",
        "data": serializer.data,
        "message": "OK"
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def orders_create(request):
    serializer = OrdersCreateSerializer(data=request.data)
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
def orders_edit(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        order = Orders.objects.get(OrderId=id)
        original_name = f"Order {order.OrderId}"
        serializer = OrdersEditSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "result": "success",
                "data": serializer.data,
                "previous_order_name": original_name,
                "message": "OK"
            }, status=status.HTTP_200_OK)
        return Response({
            "result": "error",
            "data": serializer.errors,
            "message": "Bad Request"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Orders.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Order not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def orders_delete(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        order = Orders.objects.get(OrderId=id)
        order_name = f"Order {order.OrderId}"
        order.delete()
        return Response({
            "result": "success",
            "data": {"id": id, "deleted": True, "order_name": order_name},
            "message": "Order deleted successfully"
        }, status=status.HTTP_200_OK)
    except Orders.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Order not found"
        }, status=status.HTTP_404_NOT_FOUND)