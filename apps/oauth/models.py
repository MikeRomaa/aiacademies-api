from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class GenderChoices(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    PREFER_NOT_TO_ANSWER = 'omitted'


class EthnicityChoices(models.TextChoices):
    ASIAN = 'asian'
    BLACK_OR_AFRICAN = 'black'
    CAUCASIAN = 'caucasian'
    HISPANIC_OR_LATINX = 'hispanic'
    PACIFIC_ISLANDER = 'pacific'
    PREFER_NOT_TO_ANSWER = 'omitted'


class UserManager(BaseUserManager):
    """ User Manager that knows how to create users via email instead of username """
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    username = None

    email = models.EmailField('Email Address', blank=False, null=False, unique=True)
    ethnicity = models.CharField('Ethnicity', max_length=255, choices=EthnicityChoices.choices, default=EthnicityChoices.PREFER_NOT_TO_ANSWER)
    gender = models.CharField('Gender', max_length=255, choices=GenderChoices.choices, default=GenderChoices.PREFER_NOT_TO_ANSWER)
    experience = models.IntegerField('Experience', blank=True, null=True)
    birth_year = models.IntegerField('Birth Year', blank=True, null=True)
    city_state = models.CharField('City/State', max_length=255, blank=True, null=True)
