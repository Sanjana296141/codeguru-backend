from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.review import Review
from models.project import Project
from models.finding import ReviewFinding

from services.documentation_service import (
    generate_documentation
)

from services.documentation_storage_service import (
    get_documentation,
    save_documentation,
    update_documentation
)

documentation_bp = Blueprint(
    "documentation",
    __name__,
    url_prefix="/documentation"
)


# ==========================================================
# GENERATE DOCUMENTATION
# ==========================================================

@documentation_bp.route(
    "/generate/<int:review_id>",
    methods=["POST"]
)
@jwt_required()
def generate_document(review_id):

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

    existing = get_documentation(
        review.id
    )

    if existing:

        return jsonify({

            "success": True,

            "cached": True,

            "review_id": review.id,

            "model": existing.model_used,

            "documentation": existing.documentation

        })

    findings = ReviewFinding.query.filter_by(
        review_id=review.id
    ).all()

    pylint_report = []
    bandit_report = []
    radon_report = []

    for finding in findings:

        issue = {

            "severity": finding.severity,

            "message": finding.issue,

            "line": finding.line_number

        }

        if finding.tool == "Pylint":

            pylint_report.append(issue)

        elif finding.tool == "Bandit":

            bandit_report.append(issue)

        elif finding.tool == "Radon":

            radon_report.append(issue)

    documentation = generate_documentation(

        review.project.project_name,

        pylint_report,

        bandit_report,

        radon_report

    )

    if documentation.startswith(
        "AI Service Error"
    ):

        return jsonify({

            "success": False,

            "message": documentation

        }), 503

    saved = save_documentation(

        review.id,

        documentation

    )

    return jsonify({

        "success": True,

        "cached": False,

        "review_id": review.id,

        "model": saved.model_used,

        "documentation": saved.documentation

    })


# ==========================================================
# GET DOCUMENTATION
# ==========================================================

@documentation_bp.route(
    "/<int:review_id>",
    methods=["GET"]
)
@jwt_required()
def get_document(review_id):

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

    documentation = get_documentation(
        review.id
    )

    if not documentation:

        return jsonify({

            "success": False,

            "message": "Documentation not generated yet."

        }), 404

    return jsonify({

        "success": True,

        "cached": True,

        "review_id": review.id,

        "model": documentation.model_used,

        "documentation": documentation.documentation

    })

# ==========================================================
# REGENERATE DOCUMENTATION
# ==========================================================

@documentation_bp.route(
    "/regenerate/<int:review_id>",
    methods=["POST"]
)
@jwt_required()
def regenerate_documentation(review_id):

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

    pylint_report = []
    bandit_report = []
    radon_report = []

    for finding in findings:

        issue = {

            "severity": finding.severity,

            "message": finding.issue,

            "line": finding.line_number

        }

        if finding.tool == "Pylint":

            pylint_report.append(issue)

        elif finding.tool == "Bandit":

            bandit_report.append(issue)

        elif finding.tool == "Radon":

            radon_report.append(issue)

    documentation = generate_documentation(

        review.project.project_name,

        pylint_report,

        bandit_report,

        radon_report

    )

    if documentation.startswith("AI Service Error"):

        return jsonify({

            "success": False,

            "message": documentation

        }), 503

    existing = get_documentation(
        review.id
    )

    if existing:

        existing = update_documentation(

            existing,

            documentation

        )

    else:

        existing = save_documentation(

            review.id,

            documentation

        )

    return jsonify({

        "success": True,

        "cached": False,

        "message": "Documentation regenerated successfully.",

        "review_id": review.id,

        "model": existing.model_used,

        "documentation": existing.documentation

    })