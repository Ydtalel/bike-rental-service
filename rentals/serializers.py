from rest_framework import serializers
from .models import User, Bicycle, Rental


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ['id', 'name', 'is_available']


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'user', 'bicycle', 'start_time', 'end_time', 'cost']

    def validate(self, data):
        user = data.get('user')
        if Rental.objects.filter(user=user, end_time__isnull=True).exists():
            raise serializers.ValidationError(
                'У вас уже есть активная аренда.')
        return data
