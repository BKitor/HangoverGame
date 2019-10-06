from django.urls import path
from . import views

urlpatterns = [
    path('api/quizzes', views.QuizListCreate.as_view()),
]
