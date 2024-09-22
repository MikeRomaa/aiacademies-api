import json
from itertools import chain
from operator import attrgetter

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

        # Combine lessons and quizzes, order by 'number'
        lessons = course.lessons.all()
        quizzes = course.quizzes.all()
        content = sorted(chain(lessons, quizzes), key=attrgetter('number'))

        # Find current item position in the ordered content
        current_index = next(i for i, item in enumerate(content) if item.id == lesson.id and isinstance(item, Lesson))

        # Get the next content, if any
        next_content = content[current_index + 1] if current_index < len(content) - 1 else None

        response_data = self.get_serializer(lesson).data

        if next_content:
            if isinstance(next_content, Lesson):
                response_data['next_content'] = {
                    'type': 'lesson',
                    'id': next_content.id,
                    'title': next_content.title,
                }
            elif isinstance(next_content, Quiz):
                response_data['next_content'] = {
                    'type': 'quiz',
                    'id': next_content.id,
                    'title': next_content.title,
                }
        else:
            response_data['next_content'] = None

        return Response(response_data)


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
        course = quiz.course

        # Combine lessons and quizzes, order by 'number'
        lessons = course.lessons.all()
        quizzes = course.quizzes.all()
        content = sorted(chain(lessons, quizzes), key=attrgetter('number'))

        # Find current item position in the ordered content
        current_index = next(i for i, item in enumerate(content) if item.id == quiz.id and isinstance(item, Quiz))

        # Get the next content, if any
        next_content = content[current_index + 1] if current_index < len(content) - 1 else None

        response_data = self.serializer_class(quiz).data

        if next_content:
            if isinstance(next_content, Lesson):
                response_data['next_content'] = {
                    'type': 'lesson',
                    'id': next_content.id,
                    'title': next_content.title,
                }
            elif isinstance(next_content, Quiz):
                response_data['next_content'] = {
                    'type': 'quiz',
                    'id': next_content.id,
                    'title': next_content.title,
                }
        else:
            response_data['next_content'] = None

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
