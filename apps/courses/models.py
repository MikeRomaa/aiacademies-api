import math
from datetime import timedelta

from django.db import models


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
