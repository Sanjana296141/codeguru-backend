from datetime import datetime

from extensions import db


class AIReview(db.Model):

    __tablename__ = "ai_reviews"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    review_id = db.Column(
        db.Integer,
        db.ForeignKey("reviews.id"),
        nullable=False,
        unique=True
    )

    ai_response = db.Column(
        db.Text,
        nullable=False
    )

    model_used = db.Column(
        db.String(100),
        nullable=False
    )

    generated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    review = db.relationship(
        "Review",
        backref=db.backref(
            "ai_review",
            uselist=False
        )
    )