import json
import math
from datetime import timedelta

from django.db import models

from apps.oauth.models import User


class Difficulties(models.IntegerChoices):
    EASY = 0, 'Easy'
    MODERATE = 1, 'Moderate'
    DIFFICULT = 2, 'Difficult'
    EXPERT = 3, 'Expert'


class Course(models.Model):
    name = models.CharField(max_length=255)
    banner = models.URLField()
    featured = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    difficulty = models.IntegerField(choices=Difficulties.choices, default=Difficulties.EASY)

    @property
    def enrolled(self):
        return 0

    @property
    def total_duration(self):
        return math.ceil(sum([lesson.duration for lesson in self.lessons.all()], timedelta()).seconds / 3600)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, related_name='lessons')
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    duration = models.DurationField()
    points = models.IntegerField()
    content = models.TextField()

    @property
    def duration_minutes(self):
        return self.duration.seconds // 60

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    context = models.TextField(blank=True, null=True)
    question = models.CharField(max_length=255)
    multiple_choice = models.BooleanField(default=False)
    choices = models.TextField(blank=True, null=True)  # Newline Separated
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Quiz(models.Model):
    class Meta:
        verbose_name_plural = 'Quizzes'

    course = models.ForeignKey(Course, models.CASCADE, related_name='quizzes')
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    questions = models.ManyToManyField(QuizQuestion)

    def __str__(self):
        return self.title


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, models.CASCADE, related_name='attempts')
    answers = models.TextField()  # JSON Encoded
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def score(self):
        questions = self.quiz.questions.all()
        answers = json.loads(self.answers)

        correct = 0
        for i, question in enumerate(questions):
            if answers[str(i)].strip() == question.correct_answer:
                correct += 1

        return round(correct / len(questions) * 100)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.quiz.title} - {self.score}%'
