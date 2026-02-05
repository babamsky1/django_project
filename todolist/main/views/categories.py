from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Categories
from ..serializers import CategoriesSerializer, CategoriesCreateSerializer, CategoriesEditSerializer


@api_view(['GET'])
def categories_list(request):
    categories = Categories.objects.all()
    serializer = CategoriesSerializer(categories, many=True)

    return Response({
        "result": "success",
        "data": serializer.data,
        "message": "OK"
    }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def categories_create(request):
    if request.method == 'GET':
        # Return empty form structure or template info
        return Response({
            "result": "success",
            "data": serializer.data,
            "message": "OK"
        }, status=status.HTTP_200_OK)
    
    # POST method - create employee
    print(f"Request data: {request.data}")  # Debug line
    serializer = CategoriesCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            employee = serializer.save()
            print(f"Categories created: {employee}")  # Debug line
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
def categories_edit(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        category = Categories.objects.get(CategoryId=id)
        original_name = category.CategoryName
        serializer = CategoriesEditSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "result": "success",
                "data": serializer.data,
                "previous_category_name": original_name,
                "message": "OK"
            }, status=status.HTTP_200_OK)
        return Response({
            "result": "error",
            "data": serializer.errors,
            "message": "Bad Request"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Categories.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Category not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def categories_delete(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({
                "result": "error",
                "message": "ID is required in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        category = Categories.objects.get(CategoryId=id)
        category_name = category.CategoryName
        category.delete()
        return Response({
            "result": "success",
            "data": {"id": id, "deleted": True, "category_name": category_name},
            "message": "Category deleted successfully"
        }, status=status.HTTP_200_OK)
    except Categories.DoesNotExist:
        return Response({
            "result": "error",
            "message": "Category not found"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])  # ← Match frontend POST
def categories_bulk_delete(request):
    try:
        ids = request.data.get('ids')
        if not ids:
            return Response({
                "result": "error",
                "message": "IDs are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        categories = Categories.objects.filter(CategoryId__in=ids)
        categories_count = categories.count()   
        categories.delete()
        
        return Response({
            "result": "success",
            "data": {
                "ids": ids,
                "deleted": True,
                "categories_count": categories_count
            },
            "message": "Categories deleted successfully"
        }, status=status.HTTP_200_OK)
        
    except Exception:
        return Response({
            "result": "error", 
            "message": "Bulk delete failed"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
