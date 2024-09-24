import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, views, exceptions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Course, Lesson, Quiz, QuizAttempt
from .serializers import (
    CourseSerializer,
    BaseCourseSerializer,
    LessonSerializer,
    QuizSerializer,
    QuizAttemptSerializer
)

# List all courses or create a new course
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = BaseCourseSerializer

    def get_queryset(self):
        # Prefetch related lessons and quizzes to optimize queries
        return Course.objects.prefetch_related('lessons', 'quizzes').all()


# Retrieve a single course with full details, including lessons and quizzes
class CourseInstanceView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'course_id'

    def get(self, request, *args, **kwargs):
        course = self.get_object()

        # Get lessons and quizzes for the course
        lessons = Lesson.objects.filter(course=course).order_by('number')
        quizzes = Quiz.objects.filter(course=course).order_by('number')

        lesson_serializer = LessonSerializer(lessons, many=True)
        quiz_serializer = QuizSerializer(quizzes, many=True)

        # Combine lessons and quizzes into a sorted content list
        content = sorted(
            lesson_serializer.data + quiz_serializer.data,
            key=lambda item: item['number']
        )

        # Return the full course info with sorted content
        response_data = CourseSerializer(course).data
        response_data['content'] = content

        return Response(response_data, status=status.HTTP_200_OK)


# Retrieve a single lesson by ID, and navigate to the next content
class LessonInstanceView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_url_kwarg = 'lesson_id'

    def get(self, request, *args, **kwargs):
        lesson = self.get_object()
        course = lesson.course

        # Find the next lesson or quiz in the sequence
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

        # Include next content information in the response
        response_data = self.get_serializer(lesson).data
        response_data['next_content'] = next_content

        return Response(response_data)


# Retrieve a single quiz by ID and provide navigation to the next content
class QuizInstanceView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_url_kwarg = 'quiz_id'

    def get(self, request, *args, **kwargs):
        quiz = self.get_object()
        course = quiz.course

        # Find the next quiz or lesson in the sequence
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

        # Include next content information in the response
        response_data = self.get_serializer(quiz).data
        response_data['next_content'] = next_content

        return Response(response_data)


# View for reviewing quiz attempts
class ReviewQuizAttemptView(views.APIView):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    lookup_url_kwarg = 'quiz_id'

    def get(self, request, quiz_id):
        if not self.request.user.is_authenticated:
            raise exceptions.PermissionDenied('Permission Denied')

        # Retrieve the latest quiz attempt for the user
        attempt = QuizAttempt.objects.filter(quiz_id=quiz_id, user=request.user).order_by('-timestamp').first()

        if attempt:
            serializer = QuizAttemptSerializer(attempt)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('No attempt found')


# Endpoint to get the next content (either a lesson or quiz)
@api_view(['GET'])
def get_next_content(request, course_id, current_number):
    try:
        # Get the course
        course = Course.objects.get(pk=course_id)

        # Fetch lessons and quizzes in a unified list sorted by number
        lessons = Lesson.objects.filter(course=course).order_by('number')
        quizzes = Quiz.objects.filter(course=course).order_by('number')

        # Combine lessons and quizzes into one content list
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

        # If no more content is found
        return Response({'detail': 'No more content.'}, status=status.HTTP_404_NOT_FOUND)

    except Course.DoesNotExist:
        return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
