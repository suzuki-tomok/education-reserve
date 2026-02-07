# apps/core/api/views/auth.py
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.api.serializers import LoginSerializer, MeSerializer


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "ユーザー名またはパスワードが正しくありません。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not hasattr(user, "student"):
            return Response(
                {"detail": "生徒アカウントが紐づいていません。"},
                status=status.HTTP_403_FORBIDDEN,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "student_id": user.student.id,
            "name": user.student.name,
        })


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user.student)
        return Response(serializer.data)