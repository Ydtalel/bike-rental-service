from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Bicycle, Rental
from .serializers import BicycleSerializer, RentalSerializer
from accounts.serializers import UserSerializer
from accounts.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class BicycleViewSet(viewsets.ModelViewSet):
    queryset = Bicycle.objects.all()
    serializer_class = BicycleSerializer
    permission_classes = [IsAuthenticated]


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
