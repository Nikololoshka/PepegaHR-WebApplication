from django.contrib.auth import authenticate
from django.contrib.auth.models import User as ServerUser
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK

from .models import User
from .serializers import UserSerializer


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user(request: Request):
    users = User.objects.all()
    if users is None:
        return Response({
            "users": []
        })

    serializer = UserSerializer(users, many=True)
    return Response({
        "users": serializer.data
    })


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request: Request):
    username = request.data.get("username")
    password = request.data.get("password")

    # не достает данных
    if username is None or password is None:
        return Response({
            "error": "Please provide both username and password"
        }, status=HTTP_400_BAD_REQUEST)

    # авторизация
    server_user: ServerUser = authenticate(username=username, password=password)
    if server_user is None:
        return Response({
            "error": "Invalid credentials"
        }, HTTP_401_UNAUTHORIZED)

    # получение токена
    token, _ = Token.objects.get_or_create(user=server_user)
    return Response({
        "token": token.key
    }, status=HTTP_200_OK)
