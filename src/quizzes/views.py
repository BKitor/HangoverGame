from quizzes.models import Quiz, Question
from users.models import User
from quizzes.serializers import QuizSerializer, QuestionSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response



class QuizListCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def post(self, request):
        quiz = request.data
        author = User.objects.get(uuid=quiz.get("author"))
        new_quiz = Quiz(name=quiz.get("name"), author=author)
        new_quiz.save()
        return Response(QuizSerializer(new_quiz).data)

    def get(self, request):
        quiz = Quiz.objects.all()
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)

    def put(self, request):
        return Response(None)

    def delete(self, request):
        quiz = request.data
        quiz = Quiz.objects.get(uuid=quiz.get("uuid"))
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
