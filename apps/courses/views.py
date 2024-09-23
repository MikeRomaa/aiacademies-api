import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, views, exceptions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Course, Lesson, Quiz, QuizAttempt
from .serializers import (
    BaseCourseSerializer,
    CourseSerializer,
    LessonSerializer,
    QuizSerializer,
    QuizAttemptSerializer,
)

# List all courses (brief info) or create a new course
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = BaseCourseSerializer

    def get_queryset(self):
        return Course.objects.prefetch_related('lessons', 'quizzes').all()


# Retrieve a single course with full details including lessons and quizzes
class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        course = self.get_object()

        # Get lessons and quizzes for the course
        lessons = Lesson.objects.filter(course=course).order_by('number')
        quizzes = Quiz.objects.filter(course=course).order_by('number')

        lesson_serializer = LessonSerializer(lessons, many=True)
        quiz_serializer = QuizSerializer(quizzes, many=True)

        # Combine the lessons and quizzes into a single content list
        content = sorted(
            lesson_serializer.data + quiz_serializer.data, 
            key=lambda item: item['number']
        )

        # Return the full course info including the sorted content
        response_data = CourseSerializer(course).data
        response_data['content'] = content  # Add sorted lessons and quizzes

        return Response(response_data, status=status.HTTP_200_OK)


# Retrieve a single lesson by ID
class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get(self, request, *args, **kwargs):
        lesson = self.get_object()
        return Response(self.get_serializer(lesson).data, status=status.HTTP_200_OK)


# Retrieve a single quiz by ID
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get(self, request, *args, **kwargs):
        quiz = self.get_object()
        return Response(self.get_serializer(quiz).data, status=status.HTTP_200_OK)


# Lesson Instance View
class LessonInstanceView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_url_kwarg = 'lesson_id'

    def get(self, request, *args, **kwargs):
        lesson = self.get_object()
        course = lesson.course
        next_content = self.get_next_content(course, lesson.number)

        response_data = self.get_serializer(lesson).data
        response_data['next_content'] = next_content

        return Response(response_data)

    def get_next_content(self, course, current_number):
        """
        Helper method to find the next lesson or quiz.
        """
        next_lesson = course.lessons.filter(number__gt=current_number).order_by('number').first()
        next_quiz = course.quizzes.filter(number__gt=current_number).order_by('number').first()

        if next_lesson:
            return {
                'type': 'lesson',
                'id': next_lesson.id,
                'title': next_lesson.title
            }
        elif next_quiz:
            return {
                'type': 'quiz',
                'id': next_quiz.id,
                'title': next_quiz.title
            }
        return None


# Quiz Instance View
class QuizInstanceView(views.APIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_url_kwarg = 'quiz_id'

    def get(self, request, quiz_id):
        quiz = self.get_quiz(quiz_id)
        course = quiz.course
        next_content = self.get_next_content(course, quiz.number)

        response_data = self.serializer_class(quiz).data
        response_data['next_content'] = next_content

        return Response(response_data)

    def get_quiz(self, quiz_id):
        try:
            return self.queryset.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            raise exceptions.NotFound('Quiz not found.')

    def get_next_content(self, course, current_number):
        next_quiz = course.quizzes.filter(number__gt=current_number).order_by('number').first()
        next_lesson = course.lessons.filter(number__gt=current_number).order_by('number').first()

        if next_quiz:
            return {
                'type': 'quiz',
                'id': next_quiz.id,
                'title': next_quiz.title
            }
        elif next_lesson:
            return {
                'type': 'lesson',
                'id': next_lesson.id,
                'title': next_lesson.title
            }
        return None


# Review Quiz Attempt View
class ReviewQuizAttemptView(views.APIView):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    lookup_url_kwarg = 'quiz_id'

    def get(self, request, quiz_id):
        if not self.request.user.is_authenticated:
            return Response({'detail': 'Permission Denied'}, status=401)

        query = self.queryset.filter(quiz_id=quiz_id, user=request.user)
        if query.exists():
            attempt = query.order_by('-timestamp').first()
            serializer = self.serializer_class(attempt)
            return Response(serializer.data)
        else:
            raise exceptions.NotFound('Quiz attempt not found.')


# Endpoint to handle lesson and quiz navigation
@api_view(['GET'])
def get_next_content(request, course_id, current_number):
    try:
        course = Course.objects.get(pk=course_id)

        # Fetch lessons and quizzes in a unified list sorted by number
        lessons = Lesson.objects.filter(course=course).order_by('number')
        quizzes = Quiz.objects.filter(course=course).order_by('number')

        # Combine the lessons and quizzes into one content list
        content = sorted(
            list(lessons) + list(quizzes),
            key=lambda x: x.number
        )

        # Find the current item and the next one
        for i, item in enumerate(content):
            if item.number == current_number:
                if i + 1 < len(content):
                    next_item = content[i + 1]
                    serializer = LessonSerializer(next_item) if isinstance(next_item, Lesson) else QuizSerializer(next_item)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                break

        return Response({'detail': 'No more content.'}, status=status.HTTP_404_NOT_FOUND)

    except Course.DoesNotExist:
        return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
