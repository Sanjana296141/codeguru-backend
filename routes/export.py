from flask import Blueprint, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.review import Review
from models.project import Project
from models.finding import ReviewFinding
from services.markdown_service import (
    generate_markdown
)
from services.html_service import (
    generate_html
)
from services.pdf_service import generate_pdf


export_bp = Blueprint(
    "export",
    __name__,
    url_prefix="/export"
)


@export_bp.route("/pdf/<int:review_id>", methods=["GET"])
@jwt_required()
def export_pdf(review_id):

    current_user = get_jwt_identity()

    review = (
        Review.query
        .join(Project)
        .filter(
            Review.id == review_id,
            Project.user_id == int(current_user)
        )
        .first()
    )

    if not review:

        return jsonify({
            "success": False,
            "message": "Review not found."
        }), 404

    findings = ReviewFinding.query.filter_by(
        review_id=review.id
    ).all()

    pdf_path = generate_pdf(
        review,
        findings
    )

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"review_{review.id}.pdf"
    )


#========================================================
#MARKDOWN
#=========================================================
@export_bp.route("/markdown/<int:review_id>", methods=["GET"])
@jwt_required()
def export_markdown(review_id):

    current_user = get_jwt_identity()

    review = (
        Review.query
        .join(Project)
        .filter(
            Review.id == review_id,
            Project.user_id == int(current_user)
        )
        .first()
    )

    if not review:

        return jsonify({
            "success": False,
            "message": "Review not found."
        }), 404

    findings = ReviewFinding.query.filter_by(
        review_id=review.id
    ).all()

    md_path = generate_markdown(
        review,
        findings
    )

    return send_file(
        md_path,
        as_attachment=True,
        download_name=f"review_{review.id}.md"
    )


@export_bp.route("/html/<int:review_id>", methods=["GET"])
@jwt_required()
def export_html(review_id):

    current_user = get_jwt_identity()

    review = (
        Review.query
        .join(Project)
        .filter(
            Review.id == review_id,
            Project.user_id == int(current_user)
        )
        .first()
    )

    if not review:

        return jsonify({
            "success": False,
            "message": "Review not found."
        }), 404

    findings = ReviewFinding.query.filter_by(
        review_id=review.id
    ).all()

    html_path = generate_html(
        review,
        findings
    )

    return send_file(
        html_path,
        as_attachment=True,
        download_name=f"review_{review.id}.html"
    )