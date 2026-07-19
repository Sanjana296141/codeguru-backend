from datetime import datetime

from extensions import db


class Documentation(db.Model):

    __tablename__ = "documentations"

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

    documentation = db.Column(
        db.Text,
        nullable=False
    )

    model_used = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )