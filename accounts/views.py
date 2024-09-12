from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import User
from .validators import validate_user_data
from .serializers import UserSerializer, UserLoginSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
class UserCreateView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        rlt_message = validate_user_data(request.data)
        if rlt_message is not None:
            return Response({"messgae":rlt_message}, status=400)
        
        
        user = User.objects.create_user(**request.data)
        
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        
        Response_dict = serializer.data
        Response_dict["access"] = str(refresh.access_token)
        Response_dict["refresh"] = str(refresh)
        
        return Response(Response_dict)
    
    
class UserLoginView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        
        if not user :
            return Response(
                {
                    "message":"id or password incorrect"
                },
                status=400
            )
            
        refresh = RefreshToken.for_user(user)
        
        serializer = UserLoginSerializer(user)
        
        Response_dict = serializer.data
        Response_dict["access"] = str(refresh.access_token)
        Response_dict["refresh"] = str(refresh)
        
        return Response(Response_dict)
    
class UserProfileView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, request, username):
        user = User.objects.get(username=username)
        
        serializer = UserProfileSerializer(user)
        
        return Response(serializer.data)