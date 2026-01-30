from django.shortcuts import render
from ..models import User
from ..serializers import UserSerializer

def home(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            # Serialize user data
            serializer = UserSerializer(user)
            context = {
                'logged_in': True,
                'username': user.user_name,
                'user': user,
                'user_data': serializer.data  # Serialized user data
            }
        except User.DoesNotExist:
            context = {'logged_in': False}
    else:
        context = {'logged_in': False}
    
    return render(request, 'homepage/home.html', context)