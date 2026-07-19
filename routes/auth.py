from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from utils.validators import is_valid_email
import secrets
from datetime import datetime, timedelta
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)



auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # Required fields
    if not all([name, email, password, confirm_password]):
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    # Email validation
    if not is_valid_email(email):
        return jsonify({
            "success": False,
            "message": "Invalid email address."
        }), 400

    # Password length
    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters."
        }), 400

    # Confirm password
    if password != confirm_password:
        return jsonify({
            "success": False,
            "message": "Passwords do not match."
        }), 400

    # Duplicate email
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 409

    # Create user
    user = User(
        name=name,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User registered successfully."
    }), 201



@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Required fields
    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    # Find user
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    # Check password
    if not user.check_password(password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    # Generate JWT Token
    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=24)
    )

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
        }
    }), 200

@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    current_user_id = get_jwt_identity()

    user = db.session.get(User, int(current_user_id))

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "success": False,
            "message": "Name and email are required."
        }), 400

    if not is_valid_email(email):
        return jsonify({
            "success": False,
            "message": "Invalid email address."
        }), 400

    existing_user = User.query.filter(
        User.email == email,
        User.id != user.id
    ).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already exists."
        }), 409

    user.name = name
    user.email = email

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Profile updated successfully.",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200

@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():

    current_user_id = get_jwt_identity()

    user = db.session.get(User, int(current_user_id))

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    data = request.get_json()

    old_password = data.get("old_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if not old_password or not new_password or not confirm_password:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    if not user.check_password(old_password):
        return jsonify({
            "success": False,
            "message": "Old password is incorrect."
        }), 401

    if len(new_password) < 8:
        return jsonify({
            "success": False,
            "message": "New password must be at least 8 characters."
        }), 400

    if new_password != confirm_password:
        return jsonify({
            "success": False,
            "message": "Passwords do not match."
        }), 400

    if old_password == new_password:
        return jsonify({
            "success": False,
            "message": "New password must be different from old password."
        }), 400

    user.set_password(new_password)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Password changed successfully."
    }), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    return jsonify({
        "success": True,
        "message": "Logout successful. Please remove the token from the client."
    }), 200

#forgot-password
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({
            "success": False,
            "message": "Email is required."
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "No account found with this email."
        }), 404

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Reset token generated successfully.",
        "reset_token": token
    }), 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    token = data.get("token")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if not token or not new_password or not confirm_password:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    if len(new_password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters."
        }), 400

    if new_password != confirm_password:
        return jsonify({
            "success": False,
            "message": "Passwords do not match."
        }), 400

    user = User.query.filter_by(reset_token=token).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid reset token."
        }), 400

    if user.reset_token_expiry < datetime.utcnow():
        return jsonify({
            "success": False,
            "message": "Reset token has expired."
        }), 400

    user.set_password(new_password)

    user.reset_token = None
    user.reset_token_expiry = None

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Password reset successful."
    }), 200