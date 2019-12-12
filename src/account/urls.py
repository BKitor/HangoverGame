from django.urls import path

from.views import (
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserQuizzesView
)

urlpatterns = [
    path('', UserListView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<pk>', UserDetailView.as_view()),
    path('uname/<username>', UserDetailView.as_view()),
    path('<pk>/update/', UserUpdateView.as_view()),
    path('<pk>/delete/', UserDeleteView.as_view()),
    path('<pk>/quizzes/', UserQuizzesView.as_view())
]
