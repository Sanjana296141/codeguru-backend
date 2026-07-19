from sqlalchemy import func

from models.review import Review
from models.project import Project
from models.finding import ReviewFinding


def get_review_statistics(user_id):

    reviews = (
        Review.query
        .join(Project)
        .filter(Project.user_id == int(user_id))
    )

    total_reviews = reviews.count()

    average_score = (
        reviews.with_entities(
            func.avg(Review.review_score)
        ).scalar()
        or 0
    )

    highest_score = (
        reviews.with_entities(
            func.max(Review.review_score)
        ).scalar()
        or 0
    )

    lowest_score = (
        reviews.with_entities(
            func.min(Review.review_score)
        ).scalar()
        or 0
    )

    findings = (
        ReviewFinding.query
        .join(Review)
        .join(Project)
        .filter(Project.user_id == int(user_id))
    )

    total_findings = findings.count()

    pylint = findings.filter(
        ReviewFinding.tool == "Pylint"
    ).count()

    bandit = findings.filter(
        ReviewFinding.tool == "Bandit"
    ).count()

    radon = findings.filter(
        ReviewFinding.tool == "Radon"
    ).count()

    return {

        "total_reviews": total_reviews,

        "average_score": round(average_score, 2),

        "highest_score": highest_score,

        "lowest_score": lowest_score,

        "total_findings": total_findings,

        "pylint": pylint,

        "bandit": bandit,

        "radon": radon

    }