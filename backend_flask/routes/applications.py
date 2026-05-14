from flask import Blueprint, g, jsonify, request
from sqlalchemy.exc import IntegrityError

from ..auth_utils import authenticate_token, authorize_roles
from ..extensions import db
from ..models import CV, Job, JobApplication

applications_bp = Blueprint("applications", __name__, url_prefix="/api/applications")

VALID_STATUSES = {"submitted", "reviewing", "shortlisted", "rejected", "hired"}


def application_listing_query():
    return JobApplication.query.join(JobApplication.user).join(JobApplication.job).outerjoin(JobApplication.cv)


@applications_bp.post("/")
@authenticate_token
def create_application():
    data = request.get_json(silent=True) or {}
    try:
        job_id = int(data.get("jobId"))
    except (TypeError, ValueError):
        return jsonify({"error": "Valid jobId is required"}), 400

    job = db.session.get(Job, job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    existing = JobApplication.query.filter_by(user_id=g.user.get("id"), job_id=job_id).first()
    if existing:
        return jsonify({
            "error": "You have already applied for this job",
            "data": existing.to_dict(),
        }), 409

    cv = CV.query.filter_by(user_id=g.user.get("id")).order_by(CV.created_at.desc()).first()
    application = JobApplication(
        user_id=g.user.get("id"),
        job_id=job_id,
        cv_id=cv.id if cv else None,
        cover_note=str(data.get("coverNote") or ""),
        status="submitted",
    )
    db.session.add(application)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "You have already applied for this job"}), 409

    message = (
        "Application submitted successfully"
        if cv
        else "Application submitted. Upload a CV to strengthen it."
    )
    return jsonify({"message": message, "data": application.to_dict()}), 201


@applications_bp.get("/my")
@authenticate_token
def my_applications():
    applications = (
        application_listing_query()
        .filter(JobApplication.user_id == g.user.get("id"))
        .order_by(JobApplication.created_at.desc())
        .all()
    )
    return jsonify({"data": [application.to_listing_dict() for application in applications]})


@applications_bp.get("/")
@authenticate_token
@authorize_roles(["employer", "admin"])
def list_applications():
    query = application_listing_query()
    if g.user.get("role") != "admin":
        query = query.filter(Job.posted_by_user_id == g.user.get("id"))

    applications = query.order_by(JobApplication.created_at.desc()).all()
    return jsonify({"data": [application.to_listing_dict() for application in applications]})


@applications_bp.patch("/<application_id>/status")
@authenticate_token
@authorize_roles(["employer", "admin"])
def update_application_status(application_id):
    try:
        numeric_id = int(application_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid application ID"}), 400

    data = request.get_json(silent=True) or {}
    status = str(data.get("status") or "")
    if status not in VALID_STATUSES:
        return jsonify({"error": "Invalid status"}), 400

    application = db.session.get(JobApplication, numeric_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404

    if g.user.get("role") != "admin":
        job = db.session.get(Job, application.job_id)
        if not job or job.posted_by_user_id != g.user.get("id"):
            return jsonify({"error": "Insufficient permissions"}), 403

    application.status = status
    db.session.commit()
    return jsonify({"data": application.to_dict()})
