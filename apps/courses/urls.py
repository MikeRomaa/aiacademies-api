from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.CourseListCreateView.as_view()),
    path('courses/<int:course_id>/', views.CourseInstanceView.as_view()),
    path('lessons/', views.LessonCreateView.as_view()),
    path('lessons/<int:lesson_id>/', views.LessonInstanceView.as_view()),
]
