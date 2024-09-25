from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.CourseListCreateView.as_view()),
    path('courses/<int:course_id>/', views.CourseInstanceView.as_view()),
    path('lessons/<int:lesson_id>/', views.LessonInstanceView.as_view()),
    path('quizzes/<int:quiz_id>/', views.QuizInstanceView.as_view()),
    path('quizzes/<int:quiz_id>/review/', views.ReviewQuizAttemptView.as_view()),
]
