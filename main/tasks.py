from django.core.mail import send_mail
from django.conf import settings

from main.file_utils import extract_text_from_pdf, extract_text_from_word
from main.grading_utils import grade_assignment
from main.models import Submission

import traceback

def send_assignment_email_task(subject, message, recipient_list):
    # Validate recipient_list
    if not isinstance(recipient_list, list) or not recipient_list:
        raise ValueError("recipient_list must be a non-empty list of email addresses")
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )


def grade_submission(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        extracted_text = None

        # Check if code_text is provided
        code_text = submission.code_text

        if code_text:
            extracted_text = code_text
        else:
            file = submission.file.path
            print(file)
            # Check if it's a PDF or DOCX
            file_extension = submission.file.name.lower().split('.')[-1]
            if file_extension == 'pdf':
                # Extract text from the PDF file
                extracted_text = extract_text_from_pdf(file)
            elif file_extension == 'docx':
                # Extract text from the DOCX file
                extracted_text = extract_text_from_word(file)
            else:
                raise ValueError("Unsupported file format. Only PDF and DOCX files are accepted.")

        if not extracted_text:
            raise ValueError("No valid code text or file content found for grading.")

        # Now check the assignment file type to extract the question
        assignment = submission.assignment
        if assignment.file:
            # Extract the question from the assignment file if it's available
            assignment_file_extension = assignment.file.name.lower().split('.')[-1]
            assignment_file_path = assignment.file.path
            print(assignment_file_path)
            
            if assignment_file_extension == 'pdf':
                assignment_question = extract_text_from_pdf(assignment_file_path)
            elif assignment_file_extension == 'docx':
                assignment_question = extract_text_from_word(assignment_file_path)
            else:
                raise ValueError("Unsupported assignment file format. Only PDF and DOCX files are accepted.")
        else:
            # If there's no assignment file, raise an error
            raise ValueError("Assignment file not found.")
        

        # Call the grading function
        feedback = grade_assignment(assignment_question, extracted_text)


        # Save feedback and grading result
        submission.is_graded = True
        submission.feedback = feedback
        submission.save()

        # Send an email notification to the student
        subject = "Your Submission Has Been Graded"
        message = (
            f"Dear {submission.student.username},\n\n"
            f"Your submission for the assignment '{assignment.title}' has been graded.\n"
            f"Grade: {submission.grade}\n"
            f"Feedback:\n{submission.feedback}\n\n"
            "Thank you for your submission!\n"
            "Best regards,\n"
            "Your Course Team"
        )
        recipient_list = [submission.student.email]
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
    except Submission.DoesNotExist:
        print("Submission not found.")
    except Exception as e:
        traceback.print_exc()
        print(f"Error grading submission: {e}")
