from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    duration_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        exclude = ['course', 'duration']


class BasicLessonSerializer(serializers.ModelSerializer):
    duration_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'duration_minutes', 'title', 'points']


class CourseSerializer(serializers.ModelSerializer):
    lessons = BasicLessonSerializer(many=True, read_only=True)
    total_duration = serializers.IntegerField(read_only=True)
    enrolled = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class BasicCourseSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        exclude = ['difficulty']

    def get_lessons(self, object):
        return object.lessons.count()
