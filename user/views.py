from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
class UserRegistrationView(APIView):
    def post(self, request):
        serializater = UserRegistrationSerializer(data=request.data)
        if serializater.is_valid():
            serializater.save()
            return Response(serializater.data, status=status.HTTP_201_CREATED)
        return Response(serializater.errors, status=status.HTTP_400_BAD_REQUEST)