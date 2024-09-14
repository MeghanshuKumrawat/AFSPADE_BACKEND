from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class LevelType(models.TextChoices):
    LEVEL_100 = 'Level 100', _('Level 100')
    LEVEL_200 = 'Level 200', _('Level 200')
    LEVEL_300 = 'Level 300', _('Level 300')
    LEVEL_400 = 'Level 400', _('Level 400')

class SemesterType(models.TextChoices):
    SEMESTER_1 = 'Semester 1', _('Semester 1')
    SEMESTER_2 = 'Semester 2', _('Semester 2')

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    matriculation_number = models.CharField(max_length=50, null=True, blank=True)
    level = models.CharField(max_length=50, choices=LevelType.choices, default=LevelType.LEVEL_100)
    semester = models.CharField(max_length=50, choices=SemesterType.choices, default=SemesterType.SEMESTER_1)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    image = models.FileField(upload_to='profiles/', default='profiles/default.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']