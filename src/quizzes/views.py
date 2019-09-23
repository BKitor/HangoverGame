from quizzes.models import Quiz
from quizzes.serializers import QuizSerializer
from rest_framework import generics

# Create your views here.


class QuizListCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
