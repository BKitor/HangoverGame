from users.models import User
from users.serializers import UserSerializer
from rest_framework import generics

# Create your views here.


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
