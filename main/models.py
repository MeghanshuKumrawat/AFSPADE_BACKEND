from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import LevelType, SemesterType, User

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=LevelType.choices, default=LevelType.LEVEL_100)
    semester = models.CharField(max_length=50, choices=SemesterType.choices, default=SemesterType.SEMESTER_1)
    thumbnail = models.ImageField(upload_to='static/courses', default='static/courses/default.png')

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.name} ({self.code})"

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class LanguageType(models.TextChoices):
    PYTHON = 'Python', _('Python')
    JAVA = 'Java', _('Java')

class Question(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    language = models.CharField(max_length=10, choices=LanguageType.choices, default=LanguageType.PYTHON)

    def __str__(self):
        return f"Question for {self.assignment.title}: {self.text[:50]}..."

# class Submission(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
#     student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
#     file = models.FileField(upload_to='submissions/', null=True, blank=True)
#     code_text = models.TextField(null=True, blank=True)
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     is_graded = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.student.username} - {self.assignment.title}"

# class Feedback(models.Model):
#     submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='feedback')
#     comments = models.TextField()
#     grade = models.DecimalField(max_digits=5, decimal_places=2)
#     feedback_file = models.FileField(upload_to='feedback/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Feedback for {self.submission}"

# class CourseEnrollment(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
#     student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
#     enrolled_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.student.username} enrolled in {self.course.name}"
