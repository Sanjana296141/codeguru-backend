"""
Application Constants

This file stores reusable constants used throughout the project.
Keeping constants in one place improves maintainability.
"""

# ==========================================================
# REVIEW SORTING
# ==========================================================

ALLOWED_SORT_FIELDS = [
    "date",
    "score",
    "mi"
]

ALLOWED_SORT_ORDER = [
    "asc",
    "desc"
]


# ==========================================================
# REVIEW FILTERS
# ==========================================================

ALLOWED_TOOLS = [
    "Pylint",
    "Bandit",
    "Radon"
]

ALLOWED_SEVERITIES = [
    "High",
    "Medium",
    "Low",
    "Info"
]