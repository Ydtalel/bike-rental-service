from rest_framework import serializers
from .models import Bicycle, Rental


class BicycleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Bicycle"""

    class Meta:
        model = Bicycle
        fields = ['id', 'name', 'is_available']


class RentalSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Rental"""

    def validate(self, data):
        """Проверка данных перед сохранением на предмет активной аренды"""
        user = self.context['request'].user
        rental_id = self.instance.id if self.instance else None

        if Rental.objects.filter(user=user, end_time__isnull=True).exclude(
                id=rental_id).exists():
            raise serializers.ValidationError(
                'У вас уже есть активная аренда.')
        return data

    class Meta:
        model = Rental
        fields = ['id', 'user', 'bicycle', 'start_time', 'end_time', 'cost']
        read_only_fields = ['user', 'start_time']
