import time
from pathlib import Path

from flask import Blueprint, current_app, g, jsonify, request
from werkzeug.utils import secure_filename

from ..auth_utils import authenticate_token
from ..extensions import db
from ..models import CV

cv_bp = Blueprint("cv", __name__, url_prefix="/api/cv")

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}


def save_cv_file(file_storage):
    original = secure_filename(file_storage.filename or "")
    ext = Path(original).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type")

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)
    filename = f"cv-{g.user.get('id')}-{int(time.time() * 1000)}{ext}"
    file_path = upload_folder / filename
    file_storage.save(file_path)
    return str(file_path)


@cv_bp.post("/")
@authenticate_token
def upload_cv():
    full_name = request.form.get("fullName")
    email = request.form.get("email")

    if not full_name or not email:
        return jsonify({"error": "Full name and email are required"}), 400

    existing_cv = CV.query.filter_by(user_id=g.user.get("id")).order_by(CV.created_at.desc()).first()
    file = request.files.get("cvFile")

    try:
        cv_file_path = save_cv_file(file) if file else (existing_cv.cv_file_path if existing_cv else None)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if existing_cv:
        existing_cv.full_name = full_name
        existing_cv.email = email
        existing_cv.phone = request.form.get("phone") or None
        existing_cv.linkedin_url = request.form.get("linkedinUrl") or None
        existing_cv.current_role = request.form.get("currentRole") or None
        existing_cv.expected_salary = request.form.get("expectedSalary") or None
        if cv_file_path:
            existing_cv.cv_file_path = cv_file_path
        db.session.commit()
        return jsonify({"data": existing_cv.to_dict()})

    cv = CV(
        user_id=g.user.get("id"),
        full_name=full_name,
        email=email,
        phone=request.form.get("phone") or None,
        linkedin_url=request.form.get("linkedinUrl") or None,
        current_role=request.form.get("currentRole") or None,
        expected_salary=request.form.get("expectedSalary") or None,
        cv_file_path=cv_file_path,
    )
    db.session.add(cv)
    db.session.commit()
    return jsonify({"data": cv.to_dict()}), 201


@cv_bp.get("/my")
@authenticate_token
def my_cv():
    cv = CV.query.filter_by(user_id=g.user.get("id")).order_by(CV.created_at.desc()).first()
    if not cv:
        return jsonify({"error": "CV not found"}), 404
    return jsonify({"data": cv.to_dict()})

