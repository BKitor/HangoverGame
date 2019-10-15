from quizzes.models import Quiz, Question
from users.models import User
from quizzes.serializers import QuizSerializer, QuestionSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
import json


class QuizListCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def post(self, request):
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)
        author = body.get("author")

        if not author:
            return Response("Author is a required field", status=status.HTTP_400_BAD_REQUEST)

        try:  # make sure the requested uuid exists
            author = User.objects.get(uuid=author)
        except (User.DoesNotExist, ValidationError):
            return Response("Author not found", status=status.HTTP_400_BAD_REQUEST)

        name = body.get("name")
        if not name:
            return Response("Name is a required field", status=status.HTTP_400_BAD_REQUEST)

        new_quiz = Quiz(name=name, author=author)
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
            return Response("UUID is a required field", status=status.HTTP_400_BAD_REQUEST)

        try:  # make sure the requested uuid exists
            quiz = Quiz.objects.get(uuid=uuid)
        except (Quiz.DoesNotExist, ValidationError):
            return Response("Invalid UUID", status=status.HTTP_400_BAD_REQUEST)

        return Response(QuizSerializer(quiz).data)

    def put(self, request):
        body = request.body

        # if the request has no body, then return error
        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)

        # only get objects by uuid
        uuid = body.get("uuid")
        if not uuid:
            return Response("UUID is a required field", status=status.HTTP_400_BAD_REQUEST)

        try:  # make sure the requested uuid exists
            quiz = Quiz.objects.get(uuid=body.get("uuid"))
        except (Quiz.DoesNotExist, ValidationError):
            return Response("Invalid UUID", status=status.HTTP_400_BAD_REQUEST)

        name = body.get("name")
        if name:  # if a name is included in the request, the update the name
            quiz.name = name

        # ability to change author?
        # ability to change questions?
        questions = body.get("questions")

        if not type(questions) is list:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if len(questions) > 0:
            for question in questions:
                try:
                    quiz.questions.add(Question.objects.get(uuid=question))
                except (Question.DoesNotExist, ValidationError):
                    return Response("Invalid UUID", status=status.HTTP_400_BAD_REQUEST)

        quiz.save()
        return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)

        uuid = body.get("uuid")
        if not uuid:
            return Response("UUID is a required field", status=status.HTTP_400_BAD_REQUEST)

        try:  # make sure the requested uuid exists
            quiz = Quiz.objects.get(uuid=uuid)
        except (Quiz.DoesNotExist, ValidationError):
            return Response("Invalid UUID", status=status.HTTP_400_BAD_REQUEST)

        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def post(self, request):
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)
        prompt = body.get("prompt")

        if not prompt:
            return Response("Prompt is a required field", status=status.HTTP_400_BAD_REQUEST)

        question = Question(prompt=prompt)
        question.save()

        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        body = request.body

        # if the request has no body, then return all questions
        if not body.decode('UTF-8'):
            serializer = QuestionSerializer(Question.objects.all(), many=True)
            return Response(serializer.data)

        body = json.loads(body)

        # only return a quiz by uuid
        uuid = body.get("uuid")
        if not uuid:
            return Response("UUID is a required field", status=status.HTTP_400_BAD_REQUEST)

        try:  # make sure the requested uuid exists
            question = Question.objects.get(uuid=uuid)
        except (Question.DoesNotExist, ValidationError):
            return Response("Invalid UUID", status=status.HTTP_400_BAD_REQUEST)

        return Response(QuestionSerializer(quiz).data)

    def put(self, request):
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)

        # only get objects by uuid
        uuid = body.get("uuid")
        if not uuid:
            return Response("UUID is a required field", status=status.HTTP_400_BAD_REQUEST)

        try:  # make sure the requested uuid exists
            question = Question.objects.get(uuid=body.get("uuid"))
        except (Question.DoesNotExist, ValidationError):
            return Response("Invalid UUID", status=status.HTTP_400_BAD_REQUEST)

        prompt = body.get("prompt")
        if prompt:  # if a name is included in the request, the update the name
            question.prompt = prompt

        question.save()
        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)

        uuid = body.get("uuid")
        if not uuid:
            return Response("UUID is a required field", status=status.HTTP_400_BAD_REQUEST)

        try:  # make sure the requested uuid exists
            question = Question.objects.get(uuid=uuid)
        except (Question.DoesNotExist, ValidationError):
            return Response("Invalid UUID", status=status.HTTP_400_BAD_REQUEST)

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
