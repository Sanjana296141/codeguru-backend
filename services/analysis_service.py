from services.pylint_service import run_pylint
from services.bandit_service import run_bandit
from services.radon_service import run_radon
from services.score_service import calculate_review_score
from services.review_metrics_service import save_metrics
from services.review_service import (
    create_review,
    save_findings
)


def analyze_project(project):
    """
    Runs all analysis tools and saves results.
    """

    # -----------------------------
    # Run Analysis Tools
    # -----------------------------
    pylint_report = run_pylint(project.file_path)

    bandit_report = run_bandit(project.file_path)

    # ✅ Updated Radon
    radon = run_radon(
        project.file_path
    )

    radon_report = radon["findings"]

    maintainability = radon["mi"]

    metrics = radon["metrics"]

    # -----------------------------
    # Calculate Score
    # -----------------------------
    score = calculate_review_score(
        pylint_report,
        bandit_report,
        radon_report
    )

    # -----------------------------
    # Create Review
    # -----------------------------
    review = create_review(
        project_id=project.id,
        score=score,
        summary=(
            f"Pylint: {len(pylint_report)} issue(s), "
            f"Bandit: {len(bandit_report)} issue(s), "
            f"Radon: {len(radon_report)} complexity finding(s)."
        )
    )

    # -----------------------------
    # Save Findings
    # -----------------------------
    save_findings(
        review.id,
        pylint_report,
        project.file_name,
        "Pylint"
    )

    save_findings(
        review.id,
        bandit_report,
        project.file_name,
        "Bandit"
    )

    save_findings(
        review.id,
        radon_report,
        project.file_name,
        "Radon"
    )

    # -----------------------------
    # Save Metrics
    # -----------------------------
    save_metrics(
        review,
        maintainability,
        metrics
    )

    return {
        "review": review,
        "pylint": pylint_report,
        "bandit": bandit_report,
        "radon": radon_report
    }