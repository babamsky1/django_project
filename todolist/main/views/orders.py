from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Orders
from ..serializers import OrdersSerializer, OrdersCreateSerializer, OrdersEditSerializer


@api_view(['GET', 'POST'])
def orders_list(request):
    # Check if details are requested (from query param or body)
    include_details = False
    
    if request.method == 'POST':
        # Check POST body for include parameter
        include_details = request.data.get('include', '').lower() == 'details'
    else:
        # Check query parameter for GET requests
        include_details = request.GET.get('include', '').lower() == 'details'
    
    if include_details:
        orders = Orders.objects.select_related('Customer', 'Employee', 'Shipper').all()
        
        orders_with_details = []
        for order in orders:
            order_data = {
                'OrderId': order.OrderId,
                'OrderDate': order.OrderDate,
                'CustomerName': order.Customer.CustomerName if order.Customer else 'Unknown Customer',
                'EmployeeName': f"{order.Employee.FirstName} {order.Employee.LastName}" if order.Employee else 'Unknown Employee',
                'ShipperName': order.Shipper.ShipperName if order.Shipper else 'No Shipper',
                'Customer': {
                    'CustomerId': order.Customer.CustomerId if order.Customer else None,
                    'CustomerName': order.Customer.CustomerName if order.Customer else None
                } if order.Customer else None,
                'Employee': {
                    'EmployeeId': order.Employee.EmployeeId if order.Employee else None,
                    'FirstName': order.Employee.FirstName if order.Employee else None,
                    'LastName': order.Employee.LastName if order.Employee else None
                } if order.Employee else None,
                'Shipper': {
                    'ShipperId': order.Shipper.ShipperId if order.Shipper else None,
                    'ShipperName': order.Shipper.ShipperName if order.Shipper else None
                } if order.Shipper else None
            }
            orders_with_details.append(order_data)
        
        return Response({
            "result": "success",
            "data": orders_with_details,
            "message": "OK"
        }, status=status.HTTP_200_OK)
    else:
        # Standard orders list
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
        
@api_view(['DELETE'])
def orders_bulk_delete(request):
    try:
        ids = request.data.get('ids')
        if not ids:
            return Response({
                "result": "error",
                "message": "IDs are required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        orders = Orders.objects.filter(OrderId__in=ids)
        orders_count = orders.count()
        orders.delete()
        return Response({
            "result": "success",
            "data": {"ids": ids, "deleted": True, "orders_count": orders_count},
            "message": "Orders deleted successfully"
        }, status=status.HTTP_200_OK)
    except Orders.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Orders not found"
        }, status=status.HTTP_404_NOT_FOUND)
