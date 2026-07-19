def build_ai_prompt(
    project_name,
    pylint_report,
    bandit_report,
    radon_report
):

    return f"""
You are a Senior Python Software Engineer and Code Reviewer.

Analyze ONLY the information provided below.

Project:
{project_name}

=====================
PYLINT
=====================

{pylint_report}

=====================
BANDIT
=====================

{bandit_report}

=====================
RADON
=====================

{radon_report}

Generate:

# Bug Report

# Optimization Suggestions

# Performance Recommendations

# Better Naming Suggestions

# Refactoring Advice

# Best Practices

# Security Improvements

IMPORTANT RULES

- Never invent functions.
- Never invent classes.
- Never invent variables.
- Never invent project architecture.
- Never invent examples.
- Never assume code that was not provided.
- If data is unavailable, write "Not Available".
- Base every recommendation only on supplied analysis.
- Use Markdown formatting.
"""