from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30)
    date_joined = serializers.DateTimeField()
    last_joined = serializers.DateTimeField()
    is_admin = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = '__all__'
