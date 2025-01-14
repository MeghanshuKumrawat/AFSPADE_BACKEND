from openai import OpenAI



# Set up your OpenAI API key
client = OpenAI(api_key="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")

def grade_assignment(assignment_question, student_code):
    # Construct the prompt
    system_message = (
        "You are an automated assignment grader for a programming course. "
        "The assignment is focused on Python and Java coding questions. "
        "Your role is to grade the student's submission based on correctness, efficiency, "
        "code structure, and the approach taken to solve the problem. "
        "Provide constructive and detailed feedback, highlighting what the student did well, "
        "any mistakes or inefficiencies in the code, and how they could improve their approach."
    )

    # Send the request to the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use 'gpt-4' or 'gpt-3.5-turbo'
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Assignment Question: {assignment_question}"},
            {"role": "user", "content": f"Student's Code:\n```python\n{student_code}\n```"},
        ],
        temperature=0.5,
        max_tokens=1500
    )

    # Extract and return the response
    feedback = response.choices[0].message.content
    return feedback


if __name__ == "__main__":
    # Example usage 
    assignment_question = (
        "Write a Python function is_prime(n) that returns True if n is a prime number and False otherwise. "
        "Your implementation should be efficient enough to handle numbers up to 10 million."
    )

    student_code = """
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, n):
            if n % i == 0:
                return False
        return True
    """
    # Get feedback
    feedback = grade_assignment(assignment_question, student_code)
    print("Grading Feedback:\n", feedback)