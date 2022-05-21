from rest_framework import generics

from .models import Course, Lesson
from .serializers import BaseCourseSerializer, CourseSerializer, LessonSerializer


class CourseListCreateView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = BaseCourseSerializer


class CourseInstanceView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'course_id'


class LessonInstanceView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_url_kwarg = 'lesson_id'
