from rest_framework import serializers
from .models import Bicycle, Rental


class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ['id', 'name', 'is_available']


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'user', 'bicycle', 'start_time', 'end_time', 'cost']
        read_only_fields = ['user', 'start_time']

    def validate(self, data):
        user = self.context['request'].user
        rental_id = self.instance.id if self.instance else None

        if Rental.objects.filter(user=user, end_time__isnull=True).exclude(
                id=rental_id).exists():
            raise serializers.ValidationError(
                'У вас уже есть активная аренда.')
        return data
