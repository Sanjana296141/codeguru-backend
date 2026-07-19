import ollama

from config import Config


def generate_static_summary():
    """
    Fallback summary when AI service is unavailable.
    """

    return (
        "AI review is unavailable in this environment.\n\n"
        "This report has been generated using static code analysis "
        "(Pylint, Bandit and Radon).\n\n"
        "Please review the findings below to improve your code quality, "
        "maintainability and security.\n\n"
        "For AI-generated explanations, run the application locally "
        "with Ollama installed."
    )


def generate_ai_review(prompt):
    """
    Generate AI review using local Ollama model.
    Falls back to static summary if Ollama is unavailable.
    """

    try:

        response = ollama.chat(

            model=Config.OLLAMA_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response["message"]["content"]

    except Exception as e:

        print("\n========== OLLAMA ERROR ==========")
        print(e)
        print("=================================\n")

        return generate_static_summary()