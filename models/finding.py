from extensions import db


class ReviewFinding(db.Model):
    __tablename__ = "review_findings"

    id = db.Column(db.Integer, primary_key=True)

    review_id = db.Column(
        db.Integer,
        db.ForeignKey("reviews.id"),
        nullable=False
    )

    tool = db.Column(db.String(50))

    severity = db.Column(db.String(20))

    issue = db.Column(db.Text)

    suggestion = db.Column(db.Text)

    file_name = db.Column(db.String(255))

    line_number = db.Column(db.Integer)