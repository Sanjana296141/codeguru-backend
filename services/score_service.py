def calculate_review_score(
    pylint_report,
    bandit_report,
    radon_report=None
):

    score = 10

    # ------------------
    # Pylint
    # ------------------

    for issue in pylint_report:

        issue_type = issue.get(
            "type",
            ""
        ).lower()

        penalties = {
            "fatal": 3,
            "error": 2,
            "warning": 1.5,
            "refactor": 0.5,
            "convention": 0.25
        }

        score -= penalties.get(issue_type, 0)

    # ------------------
    # Bandit
    # ------------------

    for issue in bandit_report:

        severity = issue.get(
            "issue_severity",
            ""
        ).upper()

        penalties = {
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        score -= penalties.get(
            severity,
            0
        )

    # ------------------
    # Radon
    # ------------------

    if radon_report:

        for item in radon_report:

            rank = item.get(
                "rank",
                "A"
            )

            penalties = {
                "A": 0,
                "B": 0.5,
                "C": 1,
                "D": 2,
                "E": 3,
                "F": 4
            }

            score -= penalties.get(
                rank,
                0
            )

    return max(
        0,
        round(score, 2)
    )