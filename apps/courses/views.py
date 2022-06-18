import json

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, views, exceptions
from rest_framework.response import Response

from .models import Course, Lesson, Quiz, QuizAttempt
from .serializers import BaseCourseSerializer, CourseSerializer, LessonSerializer, QuizSerializer, QuizAttemptSerializer


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


class QuizInstanceView(views.APIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_url_kwarg = 'quiz_id'

    def get_quiz(self, quiz_id):
        try:
            return self.queryset.get(id=quiz_id)
        except ObjectDoesNotExist:
            raise exceptions.NotFound()

    def get(self, request, quiz_id):
        quiz = self.get_quiz(quiz_id)
        serializer = self.serializer_class(quiz)

        return Response(serializer.data)

    def post(self, request, quiz_id):
        if not self.request.user.is_authenticated:
            self.permission_denied(self.request, 'Permission Denied', 401)

        QuizAttempt(
            user=request.user,
            quiz=self.get_quiz(quiz_id),
            answers=json.dumps(request.data),
        ).save()

        return Response()


class ReviewQuizAttemptView(views.APIView):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizSerializer
    lookup_url_kwarg = 'quiz_id'

    def get(self, request, quiz_id):
        if not self.request.user.is_authenticated:
            self.permission_denied(self.request, 'Permission Denied', 401)

        try:
            attempt = self.queryset.get(quiz_id=quiz_id, user=request.user)
        except ObjectDoesNotExist:
            raise exceptions.NotFound()

        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data)
