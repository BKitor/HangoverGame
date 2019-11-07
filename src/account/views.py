from .models import User
from .serializers import UserSerializer
from quizzes.serializers import QuizSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

# Create your views here.

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserQuizzesView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = QuizSerializer

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except (ValidationError, User.DoesNotExist):
            return Response("Invalid user ID", status=status.HTTP_400_BAD_REQUEST)
        quizzes = user.getQuizzes()
        serializer = QuizSerializer(quizzes, many=True)

        return Response(serializer.data)
