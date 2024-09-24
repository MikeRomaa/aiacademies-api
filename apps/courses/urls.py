from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseListCreateView.as_view(), name='course-list'),
    path('courses/<int:course_id>/', views.CourseInstanceView.as_view(), name='course-detail'),
    path('lessons/<int:lesson_id>/', views.LessonInstanceView.as_view(), name='lesson-detail'),
    path('quizzes/<int:quiz_id>/', views.QuizInstanceView.as_view(), name='quiz-detail'),
    path('quizzes/<int:quiz_id>/review/', views.ReviewQuizAttemptView.as_view(), name='quiz-review'),
]
