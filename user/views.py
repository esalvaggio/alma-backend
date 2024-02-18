from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserDetailsSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
class UserRegistrationView(APIView):
    def post(self, request):
        serializater = UserRegistrationSerializer(data=request.data)
        if serializater.is_valid():
            serializater.save()
            return Response(serializater.data, status=status.HTTP_201_CREATED)
        return Response(serializater.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token":token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserDetailsSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)