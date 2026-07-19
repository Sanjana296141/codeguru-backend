from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.review_filter_service import (
    filter_reviews
)
from extensions import db
from models.finding import ReviewFinding
from utils.constants import (
    ALLOWED_SORT_FIELDS,
    ALLOWED_SORT_ORDER,
    ALLOWED_TOOLS,
    ALLOWED_SEVERITIES
)
from services.review_stats_service import (
    get_review_statistics
)
from services.review_query_service import (
    get_all_reviews,
    get_review_by_id,
    delete_review_by_id,
    search_reviews,
    paginate_reviews,
    sort_reviews
)

review_bp = Blueprint(
    "review",
    __name__,
    url_prefix="/reviews"
)


# ==========================================================
# GET ALL REVIEWS
# ==========================================================
@review_bp.route("/", methods=["GET"])
@jwt_required()
def get_reviews():

    current_user = get_jwt_identity()

    reviews = get_all_reviews(current_user)

    data = []

    for review in reviews:

        project = review.project

        data.append({
            "review_id": review.id,
            "project_name": project.project_name,
            "score": review.review_score,
            "summary": review.summary,
            "created_at": review.created_at.strftime(
                "%d-%m-%Y %I:%M %p"
            )
        })

    return jsonify({
        "success": True,
        "count": len(data),
        "reviews": data
    })


# ==========================================================
# SEARCH REVIEWS
# ==========================================================
@review_bp.route("/search", methods=["GET"])
@jwt_required()
def search_review():

    current_user = get_jwt_identity()

    keyword = request.args.get("q", "").strip()

    if keyword == "":
        return jsonify({
            "success": False,
            "message": "Search keyword is required."
        }), 400

    reviews = search_reviews(
        current_user,
        keyword
    )

    data = []

    for review in reviews:

        data.append({
            "review_id": review.id,
            "project_name": review.project.project_name,
            "score": review.review_score,
            "summary": review.summary,
            "created_at": review.created_at.strftime(
                "%d-%m-%Y %I:%M %p"
            )
        })

    return jsonify({
        "success": True,
        "count": len(data),
        "reviews": data
    })


# ==========================================================
# PAGINATION
# ==========================================================
@review_bp.route("/page", methods=["GET"])
@jwt_required()
def paginate_review():

    current_user = get_jwt_identity()

    page = request.args.get("page", 1, type=int)

    per_page = request.args.get("per_page", 5, type=int)

    pagination = paginate_reviews(
        current_user,
        page,
        per_page
    )

    data = []

    for review in pagination.items:

        data.append({
            "review_id": review.id,
            "project_name": review.project.project_name,
            "score": review.review_score,
            "summary": review.summary,
            "created_at": review.created_at.strftime(
                "%d-%m-%Y %I:%M %p"
            )
        })

    return jsonify({
        "success": True,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "total_reviews": pagination.total,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "reviews": data
    })


# ==========================================================
# SORT REVIEWS
# ==========================================================
@review_bp.route("/sort", methods=["GET"])
@jwt_required()
def sort_review():

    current_user = get_jwt_identity()

    sort_by = request.args.get(
        "by",
        "date"
    )

    order = request.args.get(
        "order",
        "desc"
    )

    

    # -----------------------------
    # Validate sort field
    # -----------------------------
    if sort_by not in ALLOWED_SORT_FIELDS:

        return jsonify({
            "success": False,
            "message": "Invalid sort field. Allowed values: date, score, mi."
        }), 400

    # -----------------------------
    # Validate order
    # -----------------------------
    if order not in ALLOWED_SORT_ORDER:

        return jsonify({
            "success": False,
            "message": "Invalid sort order. Allowed values: asc, desc."
        }), 400

    reviews = sort_reviews(
        current_user,
        sort_by,
        order
    )

    data = []

    for review in reviews:

        data.append({
            "review_id": review.id,
            "project_name": review.project.project_name,
            "score": review.review_score,
            "maintainability": review.maintainability_index,
            "summary": review.summary,
            "created_at": review.created_at.strftime(
                "%d-%m-%Y %I:%M %p"
            )
        })

    return jsonify({
        "success": True,
        "count": len(data),
        "sort_by": sort_by,
        "order": order,
        "reviews": data
    })


#===================================================
#FILTER
#===================================================

@review_bp.route("/filter", methods=["GET"])
@jwt_required()
def filter_review():

    current_user = get_jwt_identity()

    tool = request.args.get("tool")

    severity = request.args.get("severity")

    tools = []
    severities = []

    if tool:
        tools = [t.strip() for t in tool.split(",")]

    if severity:
       severities = [s.strip() for s in severity.split(",")]



     # Validate Tool

    for item in tools:

     if item not in ALLOWED_TOOLS:

        return jsonify({
            "success": False,
            "message": (
                f"Invalid tool '{item}'. "
                f"Allowed values: {', '.join(ALLOWED_TOOLS)}."
            )
        }), 400

# Validate Severity

    for item in severities:

     if item not in ALLOWED_SEVERITIES:

        return jsonify({
            "success": False,
            "message": (
                f"Invalid severity '{item}'. "
                f"Allowed values: {', '.join(ALLOWED_SEVERITIES)}."
            )
        }), 400



    reviews = filter_reviews(
        current_user,
        tools,
        severities
    )

    data = []

    for review in reviews:

        data.append({

            "review_id": review.id,

            "project_name": review.project.project_name,

            "score": review.review_score,

            "maintainability": review.maintainability_index,

            "summary": review.summary,

            "created_at": review.created_at.strftime(
                "%d-%m-%Y %I:%M %p"
            )

        })

    return jsonify({

        "success": True,

        "count": len(data),

        "tool": tool,

        "severity": severity,

        "reviews": data

    })


# ==========================================================
# REVIEW STATISTICS
# ==========================================================

@review_bp.route("/statistics", methods=["GET"])
@jwt_required()
def review_statistics():

    current_user = get_jwt_identity()

    statistics = get_review_statistics(
        current_user
    )

    return jsonify({

        "success": True,

        "statistics": statistics

    })



# ==========================================================
# GET SINGLE REVIEW
# ==========================================================
@review_bp.route("/<int:review_id>", methods=["GET"])
@jwt_required()
def get_review(review_id):

    current_user = get_jwt_identity()

    review = get_review_by_id(
        current_user,
        review_id
    )

    if not review:

        return jsonify({
            "success": False,
            "message": "Review not found."
        }), 404

    findings = ReviewFinding.query.filter_by(
        review_id=review.id
    ).all()

    return jsonify({

        "success": True,

        "review": {
            "id": review.id,
            "project_name": review.project.project_name,
            "score": review.review_score,
            "summary": review.summary,
            "created_at": review.created_at.strftime(
                "%d-%m-%Y %I:%M %p"
            )
        },

        "metrics": {
            "maintainability": review.maintainability_index,
            "loc": review.loc,
            "sloc": review.sloc,
            "lloc": review.lloc,
            "comments": review.comments,
            "multi": review.multi,
            "blank": review.blank
        },

        "findings": [
            {
                "tool": finding.tool,
                "severity": finding.severity,
                "issue": finding.issue,
                "line": finding.line_number,
                "suggestion": finding.suggestion
            }

            for finding in findings
        ]

    })


# ==========================================================
# DELETE REVIEW
# ==========================================================
@review_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):

    current_user = get_jwt_identity()

    review = delete_review_by_id(
        current_user,
        review_id
    )

    if not review:

        return jsonify({
            "success": False,
            "message": "Review not found."
        }), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Review deleted successfully."
    })