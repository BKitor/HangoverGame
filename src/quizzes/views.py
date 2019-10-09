from quizzes.models import Quiz, Question
from quizzes.serializers import QuizSerializer, QuestionSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class QuizListCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def post(self, request):
        print(request.data)
        quiz = request.data
        serializer = QuizSerializer(quiz)
        print(serializer)
        return Response(quiz)

    def get(self, request):
        quiz = Quiz.objects.all()
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)

    def put(self, request):
        return Response(None)

    def delete(self, request):
        pass


class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
