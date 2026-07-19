from services.documentation_prompt_service import (
    build_documentation_prompt
)

from services.ollama_service import (
    generate_ai_review
)


def generate_documentation(
    project_name,
    pylint_report,
    bandit_report,
    radon_report
):
    """
    Generates documentation using AI.
    """

    prompt = build_documentation_prompt(
        project_name,
        pylint_report,
        bandit_report,
        radon_report
    )

    documentation = generate_ai_review(
        prompt
    )

    return documentation