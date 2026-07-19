import os
import uuid

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from extensions import db
from models.project import Project
from services.analysis_service import analyze_project
from utils.validators import allowed_file


upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/upload"
)


@upload_bp.route("/", methods=["POST"])
@jwt_required()
def upload_file():

    current_user = get_jwt_identity()

    # Check file exists
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    # Check file selected
    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected."
        }), 400

    # Validate extension
    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Only .py files are allowed."
        }), 400

    # Create unique filename
    original_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{original_filename}"

    # Create uploads folder
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, unique_filename)

    # Save uploaded file
    file.save(filepath)

    # Save project
    project = Project(
        user_id=int(current_user),
        project_name=original_filename,
        upload_type="file",
        file_name=unique_filename,
        file_path=filepath
    )

    db.session.add(project)
    db.session.commit()

    analysis = analyze_project(project)

    review = analysis["review"]

    pylint_report = analysis["pylint"]

    bandit_report = analysis["bandit"]

    radon_report = analysis["radon"]

    return jsonify({
    "success": True,
    "message": "File uploaded successfully.",

    "project": {
        "id": project.id,
        "project_name": project.project_name,
        "stored_file": project.file_name
    },

    "review": {
        "review_id": review.id,
        "score": review.review_score,
        "summary": review.summary
    },

     "metrics":{

    "maintainability":review.maintainability_index,

    "loc":review.loc,

    "sloc":review.sloc,

    "lloc":review.lloc,

    "comments":review.comments,

    "blank":review.blank

    },




    "issues": {
        "pylint": len(pylint_report),
        "bandit": len(bandit_report),
        "radon": len(radon_report),
        "total": (
            len(pylint_report)
            + len(bandit_report)
            + len(radon_report)
        )
    }

}), 201