from google import genai

from config import Config


client = genai.Client(
    api_key=Config.GEMINI_API_KEY
)


def generate_ai_review(prompt):
    """
    Generate AI review using Gemini.
    """

    try:

        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(e)
        print("==================================\n")

        return f"AI Service Error: {str(e)}"