from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import User
from .validators import validate_user_data
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
class UserCreateView(APIView):
    def post(self, request):
        
        # permission_classes = [AllowAny]
        
        # rlt_message = validate_user_data(request.data)
        
        # if rlt_message is not None:
        #     return Response({"messgae":rlt_message}, status=400)
        
        user = User.objects.create_user(**request.data)
        
        serializer = UserSerializer(user)
        
        return Response(serializer.data)