
from extensions import db
from utils.timezone import india_now

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False
    )

    review_score = db.Column(db.Float)

    summary = db.Column(db.Text)
    
    maintainability_index = db.Column(db.Float)

    loc = db.Column(db.Integer)

    sloc = db.Column(db.Integer)

    lloc = db.Column(db.Integer)

    comments = db.Column(db.Integer)

    multi = db.Column(db.Integer)

    blank = db.Column(db.Integer)




    created_at = db.Column(db.DateTime, default=india_now)

    findings = db.relationship(
        "ReviewFinding",
        backref="review",
        lazy=True,
        cascade="all, delete"
    )