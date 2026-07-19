from sqlalchemy import func
from datetime import datetime, timedelta
from models.review import Review
from models.finding import ReviewFinding
from models.ai_review import AIReview
from models.documentation import Documentation
from extensions import db
from models.project import Project

def get_dashboard_overview(user_id):

    reviews = (
        Review.query
        .join(Project)
        .filter(Project.user_id == int(user_id))
        .all()
    )

    total_projects = (
        Project.query
        .filter_by(user_id=int(user_id))
        .count()
    )

    total_reviews = len(reviews)

    total_ai_reviews = (
        AIReview.query
        .join(Review)
        .join(Project)
        .filter(Project.user_id == int(user_id))
        .count()
    )

    total_documentation = (
        Documentation.query
        .join(Review)
        .join(Project)
        .filter(Project.user_id == int(user_id))
        .count()
    )

    average_score = 0

    average_mi = 0

    if total_reviews > 0:

        average_score = round(

            sum(
                review.review_score or 0
                for review in reviews
            ) / total_reviews,

            2
        )

        average_mi = round(

            sum(
                review.maintainability_index or 0
                for review in reviews
            ) / total_reviews,

            2
        )

    return {

        "total_projects": total_projects,

        "total_reviews": total_reviews,

        "total_ai_reviews": total_ai_reviews,

        "total_documentation": total_documentation,

        "average_score": average_score,

        "average_maintainability": average_mi

    }


def get_severity_statistics(user_id):

    data = (

        ReviewFinding.query

        .join(Review)

        .join(Project)

        .filter(Project.user_id == int(user_id))

        .with_entities(

            ReviewFinding.severity,

            func.count(ReviewFinding.id)

        )

        .group_by(

            ReviewFinding.severity

        )

        .all()

    )

    statistics = {}

    for severity, count in data:

        key = severity if severity else "Unknown"

        statistics[key] = count

    return statistics


def get_tool_statistics(user_id):

    data = (

        ReviewFinding.query

        .join(Review)

        .join(Project)

        .filter(Project.user_id == int(user_id))

        .with_entities(

            ReviewFinding.tool,

            func.count(ReviewFinding.id)

        )

        .group_by(

            ReviewFinding.tool

        )

        .all()

    )

    statistics = {}

    for tool, count in data:

        key = tool if tool else "Unknown"

        statistics[key] = count

    return statistics

def get_recent_reviews(user_id):

    reviews = (

        Review.query

        .join(Project)

        .filter(
            Project.user_id == int(user_id)
        )

        .order_by(
            Review.created_at.desc()
        )

        .limit(5)

        .all()

    )

    return reviews

def get_weekly_activity(user_id):

    reviews = (
        db.session.query(
            func.date(Review.created_at),
            func.count(Review.id)
        )
        .join(Project)
        .filter(Project.user_id == int(user_id))
        .filter(
            Review.created_at >= datetime.utcnow() - timedelta(days=6)
        )
        .group_by(func.date(Review.created_at))
        .all()
    )

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    result = {
        day: 0
        for day in days
    }

    for review_date, count in reviews:

        day_name = review_date.strftime("%a")

        result[day_name] = count

    return [

        {
            "day": day,
            "reviews": result[day]
        }

        for day in days

    ]