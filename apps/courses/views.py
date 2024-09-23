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

    def get(self, request, *args, **kwargs):
        lesson = self.get_object()
        course = lesson.course
        next_lesson = course.lessons.filter(number__gt=lesson.number).order_by('number').first()
        next_quiz = course.quizzes.filter(number__gt=lesson.number).order_by('number').first()

        next_content = None
        if next_lesson:
            next_content = {
                'type': 'lesson',
                'id': next_lesson.id,
                'title': next_lesson.title
            }
        elif next_quiz:
            next_content = {
                'type': 'quiz',
                'id': next_quiz.id,
                'title': next_quiz.title
            }

        response_data = self.get_serializer(lesson).data
        response_data['next_content'] = next_content

        return Response(response_data)

class QuizInstanceView(views.APIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_url_kwarg = 'quiz_id'

    def get(self, request, quiz_id):
        quiz = self.get_quiz(quiz_id)
        course = quiz.course
        next_quiz = course.quizzes.filter(number__gt=quiz.number).order_by('number').first()
        next_lesson = course.lessons.filter(number__gt=quiz.number).order_by('number').first()

        next_content = None
        if next_quiz:
            next_content = {
                'type': 'quiz',
                'id': next_quiz.id,
                'title': next_quiz.title
            }
        elif next_lesson:
            next_content = {
                'type': 'lesson',
                'id': next_lesson.id,
                'title': next_lesson.title
            }

        response_data = self.serializer_class(quiz).data
        response_data['next_content'] = next_content

        return Response(response_data)

class ReviewQuizAttemptView(views.APIView):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizSerializer
    lookup_url_kwarg = 'quiz_id'

    def get(self, request, quiz_id):
        if not self.request.user.is_authenticated:
            self.permission_denied(self.request, 'Permission Denied', 401)

        query = self.queryset.filter(quiz_id=quiz_id, user=request.user)
        if query.count() > 0:
            attempt = query.order_by('-timestamp').first()
            serializer = QuizAttemptSerializer(attempt)
            return Response(serializer.data)
        else:
            raise exceptions.NotFound()
