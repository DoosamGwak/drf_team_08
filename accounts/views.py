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
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes


class UserLoginView(APIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.data["username"])
        if not user.is_active:
            return Response({"message": "회원탈퇴한 아이디 입니다."}, status=404)
        refresh = RefreshToken.for_user(user)
        serializer = UserLoginSerializer(user)
        Response_dict = serializer.data
        Response_dict["access"] = str(refresh.access_token)
        Response_dict["refresh"] = str(refresh)
        return Response(Response_dict, status=200)


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


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            refresh = RefreshToken.for_user(user)
            Response_dict = serializer.data
            Response_dict["access"] = str(refresh.access_token)
            Response_dict["refresh"] = str(refresh)
            return Response(Response_dict, status=201)

    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user
        data = request.data
        if not (("password" in data) and ("refresh" in data)):
            return Response(
                {
                    "password": "패스워드를 입력해주세요",
                    "refresh": "refresh토큰 값을 입력해주세요.",
                },
                status=400,
            )
        password = data["password"]
        if not user.check_password(password):
            return Response(
                {"message": "입력하신 패스워드가 일치하지 않습니다."}, status=400
            )
        refresh_token = data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        user.is_active = False
        user.save()
        return Response({"message": "계정이 성공적으로 탈퇴 되었습니다"}, status=200)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated, OwnerOnly]

    def get_object(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request, username):
        user = self.get_object(username)
        if not user.is_active:
            return Response({"message": "탈퇴한 회원입니다."}, status=404)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=200)

    def put(self, request, username):
        user = self.get_object(username)
        self.check_object_permissions(request, user)
        serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response({"message": "잘못된 데이터형식입니다."}, status=400)


class BlindReporter(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        blinded = get_object_or_404(User, username=username)
        user = request.user
        if blinded == user:
            return Response({"message": "잘못된 접근입니다."}, status=403)

        if blinded in user.blinding.all():
            user.blinding.remove(blinded)
            return Response(
                {"message": f" {username}을 블라인딩 해제 하셨습니다."}, status=200
            )

        user.blinding.add(blinded)
        return Response({"message": f" {username}을 블라인딩 하셨습니다."}, status=200)
