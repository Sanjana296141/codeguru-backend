from extensions import db
from models.ai_review import AIReview
from config import Config


def get_ai_review(review_id):
    """
    Returns saved AI review if available.
    """

    return AIReview.query.filter_by(
        review_id=review_id
    ).first()


def save_ai_review(
    review_id,
    ai_response
):
    """
    Saves AI response.
    """

    review = AIReview(

        review_id=review_id,

        ai_response=ai_response,

        model_used=Config.OLLAMA_MODEL

    )

    db.session.add(review)

    db.session.commit()

    return review


def update_ai_review(
    review,
    ai_response
):
    """
    Updates existing AI review.
    """

    review.ai_response = ai_response

    review.model_used = Config.OLLAMA_MODEL

    db.session.commit()

    return review