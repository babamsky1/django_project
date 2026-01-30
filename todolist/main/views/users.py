from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from ..models import User
from ..serializers import UserSerializer


@api_view(['GET'])
def users_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response({
        "result": "success",
        "data": serializer.data,
        "message": "OK"
    }, status=status.HTTP_200_OK)
    
# --------------------
# Login View
# --------------------
@api_view(['GET', 'POST'])
def login(request):
    # --------------------
    # GET request: show HTML form
    # --------------------
    if request.method == "GET":
        return render(request, "auth/login.html")

    # --------------------
    # POST request: handle login
    # --------------------
    data = request.data
    email = data.get("email")
    password = data.get("password")

    # Basic validation
    if not email or not password:
        return Response(
            {"error": "Email and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Try to find the user
    user = User.objects.filter(Email=email).first()
    if not user:
        return Response(
            {"error": "User not found", "message": "Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check password
    if not check_password(password, user.Password):
        return Response(    
            {"error": "Invalid email or password", "message": "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Login successful: store session
    request.session['user_id'] = str(user.UserId)
    request.session['username'] = user.FirstName

    # Success response
    return Response(
        {
            "success": f"Welcome {user.FirstName}!",
            "data": {
                "id": str(user.UserId),
                "user_name": user.FirstName,
                "email": user.Email,
                "first_name": user.FirstName,
                "last_name": user.LastName,
                "phone": user.Phone,
            },
            "message": "OK",
        },
        status=status.HTTP_200_OK
    )
    
@api_view(['GET', 'POST'])
def registration(request):
    # --------------------
    # GET request: show HTML form
    # --------------------
    if request.method == "GET":
        return render(request, "auth/register.html")

    # --------------------
    # POST request: handle registration
    # --------------------
    data = request.data
    user_name = data.get("username")
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    phone = data.get("phone", "")

    # --------------------
    # Validation
    # --------------------
    if not user_name or not email or not password:
        return Response({"error": "All required fields must be provided"}, status=status.HTTP_400_BAD_REQUEST)

    if user_name[0].isdigit():
        return Response({"error": "Username cannot start with a digit"}, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 8:
        return Response({"error": "Password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(user_name) < 4:
        return Response({"error": "Username must be at least 4 characters"}, status=status.HTTP_400_BAD_REQUEST)
    
    if phone and not phone.isdigit():
        return Response({"error": "Phone number must contain digits only"}, status=status.HTTP_400_BAD_REQUEST)

    if phone and len(phone) < 10:
        return Response({"error": "Phone number too short"}, status=status.HTTP_400_BAD_REQUEST)
    

    # Check uniqueness
    if User.objects.filter(FirstName=user_name).first():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(Email=email).first():
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(Phone=phone).first():
        return Response({"error": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # --------------------
    # Save user via serializer
    # --------------------
    user_data = {
        "UserId": user_name,
        "Email": email,
        "Password": password,
        "FirstName": first_name,
        "LastName": last_name,
        "Phone": phone
    }

    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        user = serializer.save()
        # Set session
        request.session['user_id'] = str(user.UserId)
        request.session['username'] = user.FirstName

        return Response({
            "success": f"User '{user_name}' created successfully!",
            "data": {
                "id": str(user.UserId),
                "user_name": user.FirstName,
                "email": user.Email,
                "first_name": user.FirstName,
                "last_name": user.LastName,
                "phone": user.Phone,
            },
            "message": "OK"
        }, status=status.HTTP_201_CREATED)

    # Serializer errors
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def logout(request):
    # Clear session
    request.session.flush()
    return redirect("login")  # Redirect to login page after logout


