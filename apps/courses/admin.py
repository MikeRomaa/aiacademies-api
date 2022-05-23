from django.contrib import admin

from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'number', 'title', 'duration', 'points')
