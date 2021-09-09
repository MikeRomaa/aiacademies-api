from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from aiacademies_api.permissions import IsSuperUser, IsGet
from .models import Course, Lesson
from .serializers import BasicCourseSerializer, CourseSerializer, LessonSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    # permission_classes = [IsGet | IsSuperUser]
    permission_classes = []
    authentication_classes = []

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        else:
            return self.authentication_classes

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BasicCourseSerializer
        else:
            return CourseSerializer


class CourseInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'course_id'
    # permission_classes = [IsGet | IsSuperUser]
    permission_classes = []
    authentication_classes = []


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsSuperUser]
    permission_classes = []
    authentication_classes = []


class LessonInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_url_kwarg = 'lesson_id'
    # permission_classes = [(IsGet & IsAuthenticated) | IsSuperUser]
    permission_classes = []
    authentication_classes = []
