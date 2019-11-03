from .models import User
from .serializers import UserSerializer
from quizzes.serializers import QuizSerializer
from rest_framework.response import Response

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
        user = User.objects.get(id=pk)
        quizzes = user.getQuizzes()
        serializer = QuizSerializer(quizzes, many=True)

        return Response(serializer.data)
