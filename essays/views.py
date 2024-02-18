from rest_framework import generics
from .models import Essay
from .serializers import EssaySerializer
from rest_framework.permissions import IsAuthenticated

class EssayListCreateAPIView(generics.ListCreateAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # def post(self, request, *args, **kwargs):
        # print("POST data:", request.data)  # Debugging line
        # print("Authenticated user:", self.request.user.first_name)
        # return super().post(request, *args, **kwargs)

class EssayDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer
    permission_classes = [IsAuthenticated]

class EssayListDeleteAPIView(generics.DestroyAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer
    permission_classes = [IsAuthenticated]
