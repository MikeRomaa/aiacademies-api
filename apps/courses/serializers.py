import json
from rest_framework import serializers
from .models import Course, Lesson, Quiz, QuizQuestion, QuizAttempt

class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.SerializerMethodField(read_only=True)
    duration_minutes = serializers.IntegerField(read_only=True)

    def get_course_id(self, obj: Lesson):
        return obj.course_id

    class Meta:
        model = Lesson
        exclude = ['course', 'duration']


class BasicLessonSerializer(serializers.ModelSerializer):
    duration_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'number', 'duration_minutes', 'title', 'points']


class QuizQuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField(read_only=True)

    def get_choices(self, obj: QuizQuestion):
        return obj.choices.split('\n')

    class Meta:
        model = QuizQuestion
        fields = ['context', 'question', 'multiple_choice', 'choices']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)
    course_id = serializers.SerializerMethodField(read_only=True)

    def get_course_id(self, obj: Quiz):
        return obj.course_id

    class Meta:
        model = Quiz
        fields = '__all__'


class BasicQuizSerializer(serializers.ModelSerializer):
    course_id = serializers.SerializerMethodField(read_only=True)

    def get_course_id(self, obj: Quiz):
        return obj.course_id

    class Meta:
        model = Quiz
        fields = ['id', 'number', 'title', 'course_id']


class QuizAttemptQuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['context', 'question', 'correct_answer']


class QuizAttemptSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField(read_only=True)
    answers = serializers.SerializerMethodField(read_only=True)

    def get_title(self, obj: QuizAttempt):
        return obj.quiz.title

    def get_questions(self, obj: QuizAttempt):
        questions = obj.quiz.questions.all()
        serializer = QuizAttemptQuestionSerializers(questions, many=True)
        return serializer.data

    def get_answers(self, obj: QuizAttempt):
        return json.loads(obj.answers)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'questions', 'answers', 'score']


# New Content Serializer to combine lessons and quizzes
class CourseContentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.IntegerField()
    title = serializers.CharField()
    type = serializers.CharField()


class CourseSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField(read_only=True)
    total_duration = serializers.IntegerField(read_only=True)
    enrolled = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'contents', 'total_duration', 'enrolled']

    def get_contents(self, obj: Course):
        # Get all lessons and quizzes
        lessons = obj.lessons.all().values('id', 'number', 'title').annotate(type=serializers.CharField(default='lesson'))
        quizzes = obj.quizzes.all().values('id', 'number', 'title').annotate(type=serializers.CharField(default='quiz'))

        # Combine them and sort by 'number'
        combined_contents = sorted(list(lessons) + list(quizzes), key=lambda x: x['number'])

        return CourseContentSerializer(combined_contents, many=True).data


class BaseCourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'banner', 'featured', 'num_lessons']

    def get_num_lessons(self, obj: Course):
        return obj.lessons.count()
