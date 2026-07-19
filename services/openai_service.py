from openai import OpenAI

from config import Config


client = OpenAI(
    api_key=Config.OPENAI_API_KEY
)


def generate_ai_review(prompt):

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",

                "content":
                "You are a Senior Python Code Reviewer."
            },

            {
                "role": "user",

                "content": prompt
            }

        ],

        temperature=0.3,

        max_tokens=1000

    )

    return response.choices[0].message.content