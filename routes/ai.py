from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.review import Review
from models.finding import ReviewFinding
from models.project import Project

from services.ai_review_service import generate_review
from services.ai_storage_service import (
    get_ai_review,
    save_ai_review,
    update_ai_review
)

ai_bp = Blueprint(
    "ai",
    __name__,
    url_prefix="/ai"
)


# ==========================================================
# GENERATE AI REVIEW
# ==========================================================
@ai_bp.route("/review/<int:review_id>", methods=["POST"])
@jwt_required()
def ai_review(review_id):

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

    # -----------------------------------
    # Check existing AI Review
    # -----------------------------------

    saved_review = get_ai_review(review.id)

    if saved_review:

        return jsonify({

            "success": True,

            "cached": True,

            "review_id": review.id,

            "model": saved_review.model_used,

            "ai_review": saved_review.ai_response

        }), 200

    # -----------------------------------
    # Generate AI Review
    # -----------------------------------

    ai_result = generate_review(

        review.project.project_name,

        pylint_report,

        bandit_report,

        radon_report

    )

    # -----------------------------------
    # AI Error
    # -----------------------------------

    if ai_result.startswith("AI Service Error"):

        return jsonify({

            "success": False,

            "cached": False,

            "message": ai_result

        }), 503

    # -----------------------------------
    # Save AI Review
    # -----------------------------------

    saved_review = save_ai_review(

        review.id,

        ai_result

    )

    # -----------------------------------
    # Response
    # -----------------------------------

    return jsonify({

        "success": True,

        "cached": False,

        "review_id": review.id,

        "model": saved_review.model_used,

        "ai_review": saved_review.ai_response

    }), 200


# ==========================================================
# GET SAVED AI REVIEW
# ==========================================================
@ai_bp.route("/review/<int:review_id>", methods=["GET"])
@jwt_required()
def get_saved_ai_review(review_id):

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

    ai_review = get_ai_review(review.id)

    if not ai_review:

        return jsonify({
            "success": False,
            "message": "AI review not generated yet."
        }), 404

    return jsonify({

        "success": True,

        "cached": True,

        "review_id": review.id,

        "model": ai_review.model_used,

        "ai_review": ai_review.ai_response

    }), 200

# ==========================================================
# REGENERATE AI REVIEW
# ==========================================================

@ai_bp.route("/review/<int:review_id>/regenerate", methods=["POST"])
@jwt_required()
def regenerate_ai_review(review_id):

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

    ai_result = generate_review(
        review.project.project_name,
        pylint_report,
        bandit_report,
        radon_report
    )

    if ai_result.startswith("AI Service Error"):

        return jsonify({
            "success": False,
            "message": ai_result
        }), 503

    saved_review = get_ai_review(review.id)

    if saved_review:

        saved_review = update_ai_review(
            saved_review,
            ai_result
        )

    else:

        saved_review = save_ai_review(
            review.id,
            ai_result
        )

    return jsonify({

        "success": True,

        "cached": False,

        "message": "AI review regenerated successfully.",

        "review_id": review.id,

        "model": saved_review.model_used,

        "ai_review": saved_review.ai_response

    })