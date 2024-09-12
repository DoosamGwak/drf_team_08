from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from .models import User
from .validators import validate_user_data
from .serializers import UserSerializer, UserLoginSerializer, UserProfileSerializer, UpdateUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
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
    
    
class UserLogoutView(APIView):
    def post(self, request):    
        # try:
        #     refresh_token = request.data["refresh_token"]
        #     token = RefreshToken(refresh_token)
        #     token.blacklist()

        #     return Response(
        #         {
        #             "message":"다음에 또 봐요!"
        #         },
        #         status=200
        #     )
        # except Exception as e:
        #     return Response(status=400)
        # refresh = request.data.get("refresh")
        # request.outstandintoken.token()
        # return Response({"message":"see you next time!"})
        
        try:
            request.user.auth_token.delete()
        except (AttributeError): # ObjectDoesNotExist
            pass

        logout(request)

        return Response({"success": "Successfully logged out."},
                        status=200)
        
        
class UserProfileView(APIView):
    
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def get(self, request, username):
        user = User.objects.get(username=username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    
    def delete(self, request, username):
        password = request.data.get("password")
        
        if not request.user.check_password(password):
            return Response(
                {
                    "message": "incorrect old password"
                },
                status=400
            )  
        request.user.is_active=False
        request.user.save()
        return Response({"message" : "계정이 성공적으로 탈퇴 되었습니다"})
    
    def put(self, request, *args, **kwargs):
        serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)