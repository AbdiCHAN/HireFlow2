import json
from datetime import datetime

from flask import Blueprint, g, jsonify, request
from sqlalchemy import or_

from ..auth_utils import authenticate_token
from ..extensions import db
from ..models import Job
from ..services.remotive import fetch_jobs as fetch_public_jobs

jobs_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")


def serialize_tags(tags):
    if isinstance(tags, list):
        return json.dumps([str(tag) for tag in tags[:8] if tag])
    if tags is None:
        return None
    return str(tags)


def to_number(value, fallback=None):
    try:
        if value is None or value == "":
            return fallback
        return int(value)
    except (TypeError, ValueError):
        return fallback


def to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def parse_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return value


def assign_job_fields(job, data):
    field_map = {
        "externalId": "external_id",
        "source": "source",
        "title": "title",
        "company": "company",
        "companyLogo": "company_logo",
        "category": "category",
        "rawCategory": "raw_category",
        "jobType": "job_type",
        "location": "location",
        "salary": "salary",
        "description": "description",
        "fullDescription": "full_description",
        "url": "url",
        "applicationUrl": "application_url",
        "applyUrl": "apply_url",
        "sourceName": "source_name",
    }

    for client_key, attr in field_map.items():
        if client_key in data:
            setattr(job, attr, data.get(client_key))

    if "tags" in data:
        job.tags = serialize_tags(data.get("tags"))
    if "postedAt" in data:
        job.posted_at = parse_datetime(data.get("postedAt"))
    if "featured" in data:
        job.featured = to_bool(data.get("featured"))


def sync_public_jobs(search="", category="", limit=40):
    try:
        public_jobs = fetch_public_jobs(
            search=search,
            category=category,
            limit=min(max(int(limit or 40), 1), 80),
        )

        for public_job in public_jobs:
            external_id = str(public_job.get("id") or "")
            if not external_id:
                continue

            job = Job.query.filter_by(external_id=external_id).first() or Job(external_id=external_id)
            job.source = "public"
            job.title = public_job.get("title")
            job.company = public_job.get("company")
            job.company_logo = public_job.get("companyLogo")
            job.category = public_job.get("category")
            job.raw_category = public_job.get("rawCategory")
            job.job_type = public_job.get("jobType")
            job.location = public_job.get("location")
            job.salary = public_job.get("salary")
            job.description = public_job.get("description")
            job.full_description = public_job.get("fullDescription")
            job.url = public_job.get("url")
            job.application_url = public_job.get("applicationUrl")
            job.apply_url = public_job.get("applyUrl")
            job.tags = serialize_tags(public_job.get("tags"))
            job.posted_at = parse_datetime(public_job.get("postedAt"))
            job.source_name = public_job.get("source") or "Remotive"
            job.featured = to_bool(public_job.get("featured"))

            if not job.id:
                db.session.add(job)

        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        print(f"Public job sync skipped: {exc}")


def build_job_query():
    query = Job.query
    search = request.args.get("search") or ""
    category = request.args.get("category") or ""

    if search:
        search_term = f"%{search}%"
        query = query.filter(or_(
            Job.title.like(search_term),
            Job.company.like(search_term),
            Job.description.like(search_term),
        ))

    if category and category != "All":
        query = query.filter(Job.category == category)

    return query


@jobs_bp.get("/")
def list_jobs():
    search = request.args.get("search") or ""
    category = request.args.get("category") or ""
    limit = to_number(request.args.get("limit"), 40) or 40
    offset = to_number(request.args.get("offset"))

    if request.args.get("sync") != "false":
        sync_public_jobs(search=search, category=category, limit=limit)

    query = build_job_query().order_by(Job.created_at.desc())
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)

    return jsonify({"data": [job.to_dict() for job in query.all()]})


@jobs_bp.get("/my/jobs")
@authenticate_token
def my_jobs():
    jobs = Job.query.filter_by(posted_by_user_id=g.user.get("id")).order_by(Job.created_at.desc()).all()
    return jsonify({"data": [job.to_dict() for job in jobs]})


@jobs_bp.get("/<job_id>")
def get_job(job_id):
    numeric_id = to_number(job_id)
    if numeric_id is None:
        return jsonify({"error": "Invalid job ID"}), 400

    job = db.session.get(Job, numeric_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({"data": job.to_dict()})


@jobs_bp.post("/")
@authenticate_token
def create_job():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    company = data.get("company")

    if not title or not company:
        return jsonify({"error": "Title and company are required"}), 400

    job = Job(
        external_id=data.get("externalId"),
        source=data.get("source") or "internal",
        title=title,
        company=company,
        company_logo=data.get("companyLogo"),
        category=data.get("category"),
        raw_category=data.get("rawCategory"),
        job_type=data.get("jobType"),
        location=data.get("location"),
        salary=data.get("salary"),
        description=data.get("description"),
        full_description=data.get("fullDescription") or data.get("description"),
        url=data.get("url"),
        application_url=data.get("applicationUrl"),
        apply_url=data.get("applyUrl"),
        tags=serialize_tags(data.get("tags")),
        posted_at=parse_datetime(data.get("postedAt")),
        source_name=data.get("sourceName") or "HireFlow",
        featured=to_bool(data.get("featured")) if "featured" in data else False,
        posted_by_user_id=g.user.get("id"),
    )

    db.session.add(job)
    db.session.commit()
    return jsonify({"data": job.to_dict()}), 201


@jobs_bp.put("/<job_id>")
@authenticate_token
def update_job(job_id):
    numeric_id = to_number(job_id)
    if numeric_id is None:
        return jsonify({"error": "Invalid job ID"}), 400

    job = db.session.get(Job, numeric_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    is_owner = job.posted_by_user_id == g.user.get("id")
    is_admin = g.user.get("role") == "admin"
    if not is_owner and not is_admin:
        return jsonify({"error": "Insufficient permissions"}), 403

    data = request.get_json(silent=True) or {}
    assign_job_fields(job, data)
    db.session.commit()
    return jsonify({"data": job.to_dict()})


@jobs_bp.delete("/<job_id>")
@authenticate_token
def delete_job(job_id):
    numeric_id = to_number(job_id)
    if numeric_id is None:
        return jsonify({"error": "Invalid job ID"}), 400

    job = db.session.get(Job, numeric_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    is_owner = job.posted_by_user_id == g.user.get("id")
    is_admin = g.user.get("role") == "admin"
    if not is_owner and not is_admin:
        return jsonify({"error": "Insufficient permissions"}), 403

    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted successfully"})
