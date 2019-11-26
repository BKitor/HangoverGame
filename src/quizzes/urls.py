from django.urls import path
from . import views

urlpatterns = [
    path('api/quizzes', views.QuizListCreate.as_view()),
    path('api/questions', views.QuestionListCreate.as_view()),
    path('quizzes/<pk>', views.QuizDetailView.as_view()),
]
