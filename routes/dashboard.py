from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.dashboard_service import (
    get_dashboard_overview,
    get_severity_statistics,
    get_tool_statistics,
    get_recent_reviews,
    get_weekly_activity
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


# ==========================================================
# DASHBOARD
# ==========================================================

@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def dashboard():

    current_user = get_jwt_identity()

    overview = get_dashboard_overview(
        current_user
    )

    severity = get_severity_statistics(
        current_user
    )

    tools = get_tool_statistics(
        current_user
    )

    recent = get_recent_reviews(
        current_user
    )

    recent_reviews = []

    for review in recent:

        recent_reviews.append({

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

        "overview": overview,

        "severity": severity,

        "tools": tools,

        "recent_reviews": recent_reviews

    })


# ==========================================================
# QUICK METRICS
# ==========================================================

@dashboard_bp.route("/metrics", methods=["GET"])
@jwt_required()
def dashboard_metrics():

    current_user = get_jwt_identity()

    overview = get_dashboard_overview(
        current_user
    )

    return jsonify({

        "success": True,

        "total_projects": overview["total_projects"],

        "total_reviews": overview["total_reviews"],

        "total_ai_reviews": overview["total_ai_reviews"],

        "total_documentation": overview["total_documentation"],

        "average_score": overview["average_score"],

        "average_maintainability": overview["average_maintainability"]

    })


# ==========================================================
# RECENT REVIEWS
# ==========================================================

@dashboard_bp.route("/recent", methods=["GET"])
@jwt_required()
def dashboard_recent():

    current_user = get_jwt_identity()

    reviews = get_recent_reviews(
        current_user
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

        "reviews": data

    })


# ==========================================================
# SEVERITY STATISTICS
# ==========================================================

@dashboard_bp.route("/severity", methods=["GET"])
@jwt_required()
def dashboard_severity():

    current_user = get_jwt_identity()

    return jsonify({

        "success": True,

        "severity": get_severity_statistics(
            current_user
        )

    })


# ==========================================================
# TOOL STATISTICS
# ==========================================================

@dashboard_bp.route("/tools", methods=["GET"])
@jwt_required()
def dashboard_tools():

    current_user = get_jwt_identity()

    return jsonify({

        "success": True,

        "tools": get_tool_statistics(
            current_user
        )

    })

@dashboard_bp.route("/activity", methods=["GET"])
@jwt_required()
def dashboard_activity():

    current_user = get_jwt_identity()

    return jsonify({

        "success": True,

        "activity": get_weekly_activity(current_user)

    })