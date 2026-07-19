from sqlalchemy import or_

from models.project import Project
from models.review import Review


def get_all_reviews(user_id):

    return (
        Review.query
        .join(Project)
        .filter(Project.user_id == int(user_id))
        .order_by(Review.created_at.desc())
        .all()
    )


def get_review_by_id(user_id, review_id):

    return (
        Review.query
        .join(Project)
        .filter(
            Review.id == review_id,
            Project.user_id == int(user_id)
        )
        .first()
    )


def delete_review_by_id(user_id, review_id):

    return (
        Review.query
        .join(Project)
        .filter(
            Review.id == review_id,
            Project.user_id == int(user_id)
        )
        .first()
    )

def search_reviews(user_id, keyword):

    return (
        Review.query
        .join(Project)
        .filter(
            Project.user_id == int(user_id),
            or_(
                Project.project_name.ilike(f"%{keyword}%"),
                Review.summary.ilike(f"%{keyword}%")
            )
        )
        .order_by(Review.created_at.desc())
        .all()
    )

def paginate_reviews(user_id, page, per_page):

    return (
        Review.query
        .join(Project)
        .filter(Project.user_id == int(user_id))
        .order_by(Review.created_at.desc())
        .paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    )

def sort_reviews(
    user_id,
    sort_by="date",
    order="desc"
):

    query = (
        Review.query
        .join(Project)
        .filter(
            Project.user_id == int(user_id)
        )
    )

    # -------------------------
    # Sorting Field
    # -------------------------

    if sort_by == "score":

        column = Review.review_score

    elif sort_by == "mi":

        column = Review.maintainability_index

    else:

        column = Review.created_at

    # -------------------------
    # Order
    # -------------------------

    if order == "asc":

        query = query.order_by(column.asc())

    else:

        query = query.order_by(column.desc())

    return query.all()