from django.contrib import admin

from .models import Course, Lesson, Quiz, QuizAttempt, QuizQuestion


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'number', 'title', 'duration', 'points')


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        form.base_fields['context'].help_text = "Markdown supported"
        form.base_fields['choices'].help_text = "Put each choice on its own line"
        return form


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user')
