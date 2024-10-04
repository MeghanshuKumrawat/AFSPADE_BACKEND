from django.contrib import admin
from main.models import Course, Assignment, CourseEnrollment, Submission

admin.site.register(Course)
admin.site.register(Assignment)
# admin.site.register(Question)
admin.site.register(CourseEnrollment)
admin.site.register(Submission)

