from extensions import db
from models.review import Review
from models.finding import ReviewFinding
from utils.severity import normalize_severity


def create_review(project_id, score, summary):
    """
    Create a new review for a project.
    """

    review = Review(
        project_id=project_id,
        review_score=score,
        summary=summary
    )

    db.session.add(review)
    db.session.flush()   # Generates review.id

    return review


def save_findings(review_id, findings, file_name, tool):
    """
    Save analysis findings (Pylint, Bandit, Radon, AI).
    """

    for issue in findings:

        # Handle Bandit output
        if tool == "Bandit":

                severity = issue.get("issue_severity")
                message = issue.get("issue_text")
                line = issue.get("line_number")

        # Handle Pylint output
        elif tool == "Radon":

             severity = issue.get("rank")
             message = issue.get("message")
             line = issue.get("line")

        else:

            severity = issue.get("type")
            message = issue.get("message")
            line = issue.get("line")



        # Normalize severity
        normalized = normalize_severity(
            tool,
            severity
        )

        # Create finding
        finding = ReviewFinding(
            review_id=review_id,
            tool=tool,
            severity=normalized,
            issue=message,
            suggestion="",
            file_name=file_name,
            line_number=line
        )

        db.session.add(finding)

    db.session.commit()