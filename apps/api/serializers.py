from rest_framework import serializers

from .models import User


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    email = serializers.CharField()

    def create(self, validated_data: dict):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
