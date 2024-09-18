from django.shortcuts import get_object_or_404
from .models import User
from .permissions import OwnerOnly
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UpdateUserSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(user.password)
        user.save()

        refresh = RefreshToken.for_user(user)
        Response_dict = serializer.data
        Response_dict["access"] = str(refresh.access_token)
        Response_dict["refresh"] = str(refresh)
        return Response(Response_dict, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.data["username"])

        if not user.is_active:
            return Response({"message": "회원탈퇴한 아이디 입니다."}, status=400)

        refresh = RefreshToken.for_user(user)

        serializer = UserLoginSerializer(user)

        Response_dict = serializer.data
        Response_dict["access"] = str(refresh.access_token)
        Response_dict["refresh"] = str(refresh)

        return Response(Response_dict)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated & OwnerOnly]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "다음에 또 봐요!"}, status=200)
        except Exception as e:
            return Response({"message": "잘못된 접근입니다."}, status=400)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated & OwnerOnly]

    def get(self, request, username):
        self.permission_classes = [IsAuthenticatedOrReadOnly]
        user = get_object_or_404(User, username=username)
        if not user.is_active:
            return Response({"message": "탈퇴한 회원입니다."})
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def delete(self, request, username):
        user = request.user
        password = request.data.get("password")
        if not user.check_password(password):
            return Response(
                {"message": "입력하신 패스워드가 일치하지 않습니다."}, status=400
            )
        user.is_active = False
        user.save()
        return Response({"message": "계정이 성공적으로 탈퇴 되었습니다"})

    def put(self, request, *args, **kwargs):
        serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response({"message": "잘못된 데이터형식입니다."}, status=400)

class BlindReporter(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        blinded = get_object_or_404(User, username=username)
        if blinded in request.user.blinding.all():
            return Response({"message": f" {username}을 이미 블라인딩 하셨습니다."}, status=200)
        request.user.blinding.add(blinded)
        return Response({"message": f" {username}을 블라인딩 하셨습니다."}, status=200)
    

class UnblindReporter(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        unblinded = get_object_or_404(User, username=username)
        if unblinded  not in request.user.blinding.all():
            return Response({"message": f" {username}을 이미 블라인딩 해제 하셨습니다."}, status=200)
        request.user.blinding.remove(unblinded)
        return Response({"message": f" {username}을 블라인딩 해제 하셨습니다."}, status=200)
        