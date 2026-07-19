from models.project import Project
from models.review import Review
from models.finding import ReviewFinding


def filter_reviews(
    user_id,
    tools=None,
    severities=None
):

    query = (
        Review.query
        .join(Project)
        .join(ReviewFinding)
        .filter(Project.user_id == int(user_id))
    )

    if tools:
        query = query.filter(
            ReviewFinding.tool.in_(tools)
        )

    if severities:
        query = query.filter(
            ReviewFinding.severity.in_(severities)
        )

    return (
        query
        .distinct()
        .order_by(Review.created_at.desc())
        .all()
    )