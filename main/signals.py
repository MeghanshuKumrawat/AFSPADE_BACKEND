from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment, CourseEnrollment
from .tasks import send_assignment_email_task

@receiver(post_save, sender=Assignment)
def send_assignment_email(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        # Get the list of enrolled students' emails
        enrolled_students = CourseEnrollment.objects.filter(course=course)
        student_emails = [enrollment.student.email for enrollment in enrolled_students if enrollment.student.email]
        print(student_emails)
        # Send email asynchronously if there are students enrolled

        
        if student_emails:
            subject = f"New Assignment: {instance.title}"
            message = f"A new assignment has been created for your course {course.name}. The deadline is {instance.deadline.date()}."
            
            print(subject, message, student_emails)  # Add this to debug
            # Ensure student_emails is a list of valid email addresses
            if not isinstance(student_emails, list) or not student_emails:
                raise ValueError("student_emails must be a non-empty list")
            # Use  to send the email asynchronously
            send_assignment_email_task(subject, message, student_emails)
