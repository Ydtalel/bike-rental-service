import math
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Bicycle, Rental
from .serializers import BicycleSerializer, RentalSerializer
from accounts.serializers import UserSerializer
from accounts.models import User
from datetime import datetime


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с пользователями (User)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class BicycleViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с велосипедами (Bicycle)"""

    queryset = Bicycle.objects.filter(is_available=True)
    serializer_class = BicycleSerializer
    permission_classes = [IsAuthenticated]


class RentalViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с арендой велосипедов (Rental)"""

    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Сохранение аренды с указанием текущего пользователя"""
        serializer.save(user=self.request.user)

    def return_bicycle(self, request, pk=None):
        """Обновление данных по аренде при возврате велосипеда"""
        rental = self.get_object()
        rental.end_time = now()
        start_time = rental.start_time
        cost = self.calculate_rental_cost(start_time, rental.end_time)

        rental.cost = cost
        rental.save()

        serializer = self.get_serializer(rental)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Частичное обновление данных по аренде велосипеда"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)

        end_time_str = request.data.get('end_time')

        if end_time_str:
            end_time = datetime.fromisoformat(end_time_str)
        else:
            end_time = now()

        start_time = instance.start_time
        if start_time and end_time:
            instance.end_time = end_time
            instance.cost = self.calculate_rental_cost(start_time, end_time)

        instance.save()
        return Response(serializer.data)

    def calculate_rental_cost(self, start_time, end_time):
        """Расчет стоимости аренды на основе времени аренды"""
        duration = end_time - start_time
        total_seconds = duration.total_seconds()

        total_hours = math.ceil(total_seconds / 3600)
        first_hour_cost = 100

        if total_hours == 1:
            return first_hour_cost
        total_cost = first_hour_cost + (total_hours - 1) * 100
        return total_cost

    @action(detail=False, methods=['GET'], url_path='user')
    def user_history(self, request):
        """ Получение истории аренд пользователя"""
        user = request.user
        rentals = Rental.objects.filter(user=user).order_by('-start_time')
        serializer = self.get_serializer(rentals, many=True)
        return Response(serializer.data)
