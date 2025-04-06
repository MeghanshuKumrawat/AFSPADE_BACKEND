from openai import OpenAI
import json


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
        "any mistakes or inefficiencies in the code, and how they could improve their approach. "
        "Give your response in JSON format with two keys: 'feedback' containing your detailed review, "
        "and 'grade' representing the overall grade for the submission out of 100. "
        "\n\n"
        "IMPORTANT INSTRUCTIONS:\n"
        "- Do not include any text before or after the JSON output. Only return the JSON object.\n"
        "- The 'feedback' key should contain a full explanation without starting with phrases like "
        "'The code shows...' or 'The solution shows...'. Just begin with the relevant points.\n"
        "- Do not make assumptions or speculate. Only grade based on what is present in the code.\n"
        "- Make sure the JSON is syntactically correct, and avoid trailing commas or unquoted keys.\n"
        "- The 'grade' should be a numeric value between 0 and 100."
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

    # # Extract and return the response
    feedback = json.loads(response.choices[0].message.content.strip())
    print(feedback)
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
    print("Grading Feedback:\n", feedback['feedback'])
    print("Grading:\n", feedback['grade'])