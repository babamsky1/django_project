from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Employees
from ..serializers import EmployeesSerializer, EmployeesCreateSerializer, EmployeesEditSerializer


@api_view(['GET'])
def employees_list(request):
    employees = Employees.objects.all()
    serializer = EmployeesSerializer(employees, many=True)

    return Response({
        "result": "success",
        "data": serializer.data,
        "message": "OK"
    }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def employees_create(request):
    if request.method == 'GET':
        # Return empty form structure or template info
        return Response({
            "result": "success",
            "data": serializer.data,
            "message": "OK"
        }, status=status.HTTP_200_OK)
    
    # POST method - create employee
    print(f"Request data: {request.data}")  # Debug line
    serializer = EmployeesCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            employee = serializer.save()
            print(f"Employee created: {employee}")  # Debug line
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
def employees_edit(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        employee = Employees.objects.get(EmployeeId=id)
        original_name = f"{employee.FirstName} {employee.LastName}"
        serializer = EmployeesEditSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "result": "success",
                "data": serializer.data,
                "previous_employee_name": original_name,
                "message": "OK"
            }, status=status.HTTP_200_OK)
        return Response({
            "result": "error",
            "data": serializer.errors,
            "message": "Bad Request"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Employees.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Employee not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def employees_delete(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        employee = Employees.objects.get(EmployeeId=id)
        employee_name = f"{employee.FirstName} {employee.LastName}"
        employee.delete()
        return Response({
            "result": "success",
            "data": {"id": id, "deleted": True, "employee_name": employee_name},
            "message": "Employee deleted successfully"
        }, status=status.HTTP_200_OK)
    except Employees.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Employee not found"
        }, status=status.HTTP_404_NOT_FOUND)
