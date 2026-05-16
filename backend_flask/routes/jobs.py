from flask import request, jsonify
from extensions import db
from models import Job
from auth_utils import authenticate_token, authorize_role
import json


def serialize_tags(tags):
    """Serialize tags to JSON string"""
    if isinstance(tags, list):
        return json.dumps(tags[:8])
    return str(tags) if tags else None


def serialize_job(job, full=False):
    """Serialize a Job model to dict"""
    data = {
        'id': job.id,
        'externalId': job.external_id,
        'source': job.source,
        'title': job.title,
        'company': job.company,
        'companyLogo': job.company_logo,
        'category': job.category,
        'jobType': job.job_type,
        'location': job.location,
        'salary': job.salary,
        'description': job.description,
        'fullDescription': job.full_description,
        'tags': job.tags,
        'postedAt': job.posted_at.isoformat() if job.posted_at else None,
        'sourceName': job.source_name,
        'featured': job.featured,
        'createdAt': job.created_at.isoformat(),
        'updatedAt': job.updated_at.isoformat()
    }
    if full:
        data['postedByUserId'] = job.posted_by_user_id
    return data


def is_job_owner_or_admin(job, user):
    """Check if user owns the job or is an admin"""
    return job.posted_by_user_id == user.get('id') or user.get('role') == 'admin'


def register_job_routes(app):
    """Register all job routes to Flask app"""

    @app.route('/api/jobs', methods=['GET'])
    def list_jobs():
        """List jobs with search and filters"""
        try:
            search = request.args.get('search', '').strip()
            category = request.args.get('category', '').strip()
            limit = min(int(request.args.get('limit', 40)), 80)
            offset = int(request.args.get('offset', 0))

            query = Job.query

            if search:
                search_filter = f'%{search}%'
                query = query.filter(db.or_(
                    Job.title.ilike(search_filter),
                    Job.company.ilike(search_filter),
                    Job.description.ilike(search_filter)
                ))

            if category:
                query = query.filter(Job.category.ilike(f'%{category}%'))

            total = query.count()
            jobs = query.order_by(Job.posted_at.desc()).limit(limit).offset(offset).all()

            return jsonify({
                'data': [serialize_job(j) for j in jobs],
                'total': total,
                'limit': limit,
                'offset': offset
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @app.route('/api/jobs/<int:job_id>', methods=['GET'])
    def get_job(job_id):
        """Get single job details"""
        try:
            job = Job.query.get(job_id)
            if not job:
                return jsonify({'error': 'Job not found'}), 404

            return jsonify({'data': serialize_job(job, full=True)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @app.route('/api/jobs', methods=['POST'])
    @authenticate_token
    @authorize_role('employer', 'admin')
    def create_job():
        """Create new internal job"""
        try:
            user = request.user
            data = request.get_json() or {}

            title = data.get('title', '').strip()
            company = data.get('company', '').strip()

            if not title or len(title) < 3:
                return jsonify({'error': 'Job title required (min 3 chars)'}), 400
            if not company:
                return jsonify({'error': 'Company name required'}), 400

            def clean(key):
                return data.get(key, '').strip() or None

            job = Job(
                source='internal',
                title=title,
                company=company,
                company_logo=clean('companyLogo'),
                category=clean('category'),
                job_type=clean('jobType'),
                location=clean('location'),
                salary=clean('salary'),
                description=clean('description'),
                full_description=clean('fullDescription'),
                tags=serialize_tags(data.get('tags')),
                source_name='HireFlow',
                featured=bool(data.get('featured', False)),
                posted_by_user_id=user.get('id')
            )

            db.session.add(job)
            db.session.commit()

            return jsonify({
                'message': 'Job posted successfully',
                'data': {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'location': job.location,
                    'createdAt': job.created_at.isoformat()
                }
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    @app.route('/api/jobs/<int:job_id>', methods=['PUT'])
    @authenticate_token
    def update_job(job_id):
        """Update job (owner or admin only)"""
        try:
            user = request.user
            job = Job.query.get(job_id)

            if not job:
                return jsonify({'error': 'Job not found'}), 404
            if not is_job_owner_or_admin(job, user):
                return jsonify({'error': 'Insufficient permissions'}), 403

            data = request.get_json() or {}

            if 'title' in data:
                title = data['title'].strip()
                if not title or len(title) < 3:
                    return jsonify({'error': 'Title must be at least 3 chars'}), 400
                job.title = title

            for attr, key in [
                ('description', 'description'),
                ('full_description', 'fullDescription'),
                ('salary', 'salary'),
                ('location', 'location'),
            ]:
                if key in data:
                    setattr(job, attr, data[key].strip() or None)

            if 'tags' in data:
                job.tags = serialize_tags(data['tags'])
            if 'featured' in data:
                job.featured = bool(data['featured'])

            db.session.commit()

            return jsonify({'message': 'Job updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    @app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
    @authenticate_token
    def delete_job(job_id):
        """Delete job (owner or admin only)"""
        try:
            user = request.user
            job = Job.query.get(job_id)

            if not job:
                return jsonify({'error': 'Job not found'}), 404
            if not is_job_owner_or_admin(job, user):
                return jsonify({'error': 'Insufficient permissions'}), 403

            db.session.delete(job)
            db.session.commit()

            return jsonify({'message': 'Job deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
