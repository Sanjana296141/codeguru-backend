from services.ai_prompt_service import build_ai_prompt
from services.ollama_service import generate_ai_review


def generate_review(
    project_name,
    pylint_report,
    bandit_report,
    radon_report
):
    """
    Generates AI review using OLLAMA.
    """

    prompt = build_ai_prompt(
        project_name,
        pylint_report,
        bandit_report,
        radon_report
    )

    ai_response = generate_ai_review(
        prompt
    )

    return ai_response