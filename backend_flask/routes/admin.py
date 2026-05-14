from flask import Blueprint, jsonify

from ..auth_utils import authenticate_token, authorize_roles
from ..models import CV, Job, JobApplication, User

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/overview")
@authenticate_token
@authorize_roles(["admin"])
def overview():
    users = User.query.order_by(User.created_at.desc()).all()
    jobs = Job.query.order_by(Job.created_at.desc()).limit(500).all()
    cvs = CV.query.join(CV.user).order_by(CV.created_at.desc()).all()
    applications = (
        JobApplication.query
        .join(JobApplication.user)
        .join(JobApplication.job)
        .outerjoin(JobApplication.cv)
        .order_by(JobApplication.created_at.desc())
        .all()
    )

    safe_users = [user.to_admin_dict() for user in users]

    return jsonify({
        "data": {
            "stats": {
                "users": len(safe_users),
                "jobs": len(jobs),
                "cvs": len(cvs),
                "applications": len(applications),
            },
            "users": safe_users,
            "jobs": [job.to_dict() for job in jobs],
            "cvs": [cv.to_admin_dict() for cv in cvs],
            "applications": [application.to_listing_dict() for application in applications],
        }
    })

