from quizzes.models import Quiz, Question
from users.models import User
from quizzes.serializers import QuizSerializer, QuestionSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
import json


class QuizListCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def post(self, request):
        quiz = request.data

        author = quiz.get("author")

        try:  # make sure the requested uuid exists
            author = User.objects.get(uuid=author)
        except User.DoesNotExist:
            return Response(None)  # should add some kind of error

        new_quiz = Quiz(name=quiz.get("name"), author=author)
        new_quiz.save()

        return Response(QuizSerializer(new_quiz).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        body = request.body

        # if the request has no body, then return all quizzes
        if not body.decode('UTF-8'):
            serializer = QuizSerializer(Quiz.objects.all(), many=True)
            return Response(serializer.data)

        body = json.loads(body)

        # only return a quiz by uuid
        uuid = body.get("uuid")
        if not uuid:
            return Response(None) # should add some kind of error

        try: # make sure the requested uuid exists
            quiz = Quiz.objects.get(uuid=uuid)
        except Quiz.DoesNotExist:
            return Response(None) # should add some kind of error

        return Response(QuizSerializer(quiz).data)

    def put(self, request):
        body = request.body

        # if the request has no body, then return error
        if not body.decode('UTF-8'):
            return Response(None) # should add some kind of error

        body = json.loads(body)

        # only get objects by uuid
        uuid = body.get("uuid")
        if not uuid:
            return Response(None)  # should add some kind of error

        try:  # make sure the requested uuid exists
            quiz = Quiz.objects.get(uuid=body.get("uuid"))
        except Quiz.DoesNotExist:
            return Response(None)  # should add some kind of error

        name = body.get("name")
        if name:  # if a name is included in the request, the update the name
            quiz.name = name
            quiz.save()

        # ability to change author?
        # ability to change questions?

        return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        quiz = request.data

        try:  # make sure the requested uuid exists
            quiz = Quiz.objects.get(uuid=quiz.get("uuid"))
        except Quiz.DoesNotExist:
            return Response(None)  # should add some kind of error

        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
