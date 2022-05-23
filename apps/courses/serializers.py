from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.SerializerMethodField(read_only=True)
    duration_minutes = serializers.IntegerField(read_only=True)

    def get_course_id(self, obj: Lesson):
        return obj.course_id

    class Meta:
        model = Lesson
        exclude = ['number', 'course', 'duration']


class BasicLessonSerializer(serializers.ModelSerializer):
    duration_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'number', 'duration_minutes', 'title', 'points']


class CourseSerializer(serializers.ModelSerializer):
    lessons = BasicLessonSerializer(many=True, read_only=True)
    total_duration = serializers.IntegerField(read_only=True)
    enrolled = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class BaseCourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'banner', 'featured', 'num_lessons']

    def get_num_lessons(self, obj: Course):
        return obj.lessons.count()
