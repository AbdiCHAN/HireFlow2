from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint, text

from .extensions import db


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def serialize_datetime(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return value.isoformat()


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        db.Index("idx_users_email", "email"),
        db.Index("idx_users_username", "username"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False, default="job_seeker", server_default="job_seeker")
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow, server_default=db.func.current_timestamp())

    def to_auth_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
        }

    def to_model_dict(self):
        return {
            **self.to_auth_dict(),
            "passwordHash": self.password_hash,
            "createdAt": serialize_datetime(self.created_at),
        }

    def to_admin_dict(self):
        return {
            **self.to_auth_dict(),
            "createdAt": serialize_datetime(self.created_at),
        }


class Job(db.Model):
    __tablename__ = "jobs"
    __table_args__ = (
        db.Index("idx_jobs_source", "source"),
        db.Index("idx_jobs_posted_by_user_id", "posted_by_user_id"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    external_id = db.Column(db.Text)
    source = db.Column(db.Text, nullable=False, default="internal", server_default="internal")
    title = db.Column(db.Text, nullable=False)
    company = db.Column(db.Text, nullable=False)
    company_logo = db.Column(db.Text)
    category = db.Column(db.Text)
    raw_category = db.Column(db.Text)
    job_type = db.Column(db.Text)
    location = db.Column(db.Text)
    salary = db.Column(db.Text)
    description = db.Column(db.Text)
    full_description = db.Column(db.Text)
    url = db.Column(db.Text)
    application_url = db.Column(db.Text)
    apply_url = db.Column(db.Text)
    tags = db.Column(db.Text)
    posted_at = db.Column(db.Text)
    source_name = db.Column(db.Text, default="Remotive", server_default="Remotive")
    featured = db.Column(db.Boolean, nullable=False, default=False, server_default=text("0"))
    posted_by_user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
        server_default=db.func.current_timestamp(),
    )

    poster = db.relationship("User", backref=db.backref("posted_jobs", passive_deletes=True))

    def to_dict(self):
        return {
            "id": self.id,
            "externalId": self.external_id,
            "source": self.source,
            "title": self.title,
            "company": self.company,
            "companyLogo": self.company_logo,
            "category": self.category,
            "rawCategory": self.raw_category,
            "jobType": self.job_type,
            "location": self.location,
            "salary": self.salary,
            "description": self.description,
            "fullDescription": self.full_description,
            "url": self.url,
            "applicationUrl": self.application_url,
            "applyUrl": self.apply_url,
            "tags": self.tags,
            "postedAt": serialize_datetime(self.posted_at),
            "sourceName": self.source_name,
            "featured": bool(self.featured),
            "postedByUserId": self.posted_by_user_id,
            "createdAt": serialize_datetime(self.created_at),
            "updatedAt": serialize_datetime(self.updated_at),
        }


class CV(db.Model):
    __tablename__ = "cvs"
    __table_args__ = (db.Index("idx_cvs_user_id", "user_id"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text)
    linkedin_url = db.Column(db.Text)
    current_role = db.Column(db.Text)
    expected_salary = db.Column(db.Text)
    cv_file_path = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
        server_default=db.func.current_timestamp(),
    )

    user = db.relationship("User", backref=db.backref("cvs", passive_deletes=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "linkedin_url": self.linkedin_url,
            "current_role": self.current_role,
            "expected_salary": self.expected_salary,
            "cv_file_path": self.cv_file_path,
            "created_at": serialize_datetime(self.created_at),
            "updated_at": serialize_datetime(self.updated_at),
        }

    def to_admin_dict(self):
        user = self.user
        return {
            **self.to_dict(),
            "username": user.username if user else None,
            "user_email": user.email if user else None,
        }


class JobApplication(db.Model):
    __tablename__ = "job_applications"
    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_job_applications_user_job"),
        db.Index("idx_job_applications_user_id", "user_id"),
        db.Index("idx_job_applications_job_id", "job_id"),
        db.Index("idx_job_applications_status", "status"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    cv_id = db.Column(db.Integer, db.ForeignKey("cvs.id", ondelete="SET NULL"))
    cover_note = db.Column(db.Text)
    status = db.Column(db.Text, nullable=False, default="submitted", server_default="submitted")
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
        server_default=db.func.current_timestamp(),
    )

    user = db.relationship("User", backref=db.backref("applications", passive_deletes=True))
    job = db.relationship("Job", backref=db.backref("applications", passive_deletes=True))
    cv = db.relationship("CV", foreign_keys=[cv_id])

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "jobId": self.job_id,
            "cvId": self.cv_id,
            "coverNote": self.cover_note,
            "status": self.status,
            "createdAt": serialize_datetime(self.created_at),
            "updatedAt": serialize_datetime(self.updated_at),
        }

    def to_listing_dict(self):
        user = self.user
        job = self.job
        cv = self.cv
        return {
            **self.to_dict(),
            "applicantName": user.username if user else None,
            "applicantEmail": user.email if user else None,
            "jobTitle": job.title if job else None,
            "company": job.company if job else None,
            "jobLocation": job.location if job else None,
            "postedByUserId": job.posted_by_user_id if job else None,
            "cvFullName": cv.full_name if cv else None,
            "cvEmail": cv.email if cv else None,
            "cvPhone": cv.phone if cv else None,
            "currentRole": cv.current_role if cv else None,
            "expectedSalary": cv.expected_salary if cv else None,
            "cvFilePath": cv.cv_file_path if cv else None,
        }


class ApiKey(db.Model):
    __tablename__ = "api_keys"
    __table_args__ = (
        db.Index("idx_api_keys_user_id", "user_id"),
        db.Index("idx_api_keys_key_hash", "key_hash"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    key_hash = db.Column(db.Text, nullable=False, unique=True)
    key_prefix = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow, server_default=db.func.current_timestamp())
    last_used_at = db.Column(db.DateTime)
    revoked_at = db.Column(db.DateTime)

    user = db.relationship("User", backref=db.backref("api_keys", passive_deletes=True))

    def to_public_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "name": self.name,
            "keyPrefix": self.key_prefix,
            "createdAt": serialize_datetime(self.created_at),
            "lastUsedAt": serialize_datetime(self.last_used_at),
            "revokedAt": serialize_datetime(self.revoked_at),
        }
