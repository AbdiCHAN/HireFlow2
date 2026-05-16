"""
Jobs Routes Handle job-related API endpoints 
"""
from flask import request
from extensions import db
from models import Job
from utils.auth import authenticate_token, authorize_role
from utils.responses import success_response, error_response, paginated_response
from utils import serialize_tags, validate_string


def register_job_routes(app):
    @app.route('/api/jobs', methods=['GET'])
    def list_jobs():
        try:
            search = request.args.get('search', '').strip()
            category = request.args.get('category', '').strip()
            limit = min(int(request.args.get('limit', 40)), 80)
            offset = int(request.args.get('offset', 0))

            if limit < 1 or offset < 0:
                return error_response('Invalid limit or offset', 400)

            query = Job.query
            if search:
                search_filter = f'%{search}%'
                query = query.filter(
                    db.or_(
                        Job.title.ilike(search_filter),
                        Job.company.ilike(search_filter),
                        Job.description.ilike(search_filter)
                    )
                )
            if category:
                category_filter = f'%{category}%'
                query = query.filter(Job.category.ilike(category_filter))

            total = query.count()
            jobs = query.order_by(Job.posted_at.desc(), Job.created_at.desc()).limit(limit).offset(offset).all()
            jobs_data = [
                {
                    'id': j.id,
                    'externalId': j.external_id,
                    'source': j.source,
                    'title': j.title,
                    'company': j.company,
                    'companyLogo': j.company_logo,
                    'category': j.category,
                    'rawCategory': j.raw_category,
                    'jobType': j.job_type,
                    'location': j.location,
                    'salary': j.salary,
                    'description': j.description,
                    'fullDescription': j.full_description,
                    'url': j.url,
                    'applicationUrl': j.application_url,
                    'applyUrl': j.apply_url,
                    'tags': j.tags,
                    'postedAt': j.posted_at.isoformat() if j.posted_at else None,
                    'sourceName': j.source_name,
                    'featured': j.featured,
                    'postedByUserId': j.posted_by_user_id,
                    'createdAt': j.created_at.isoformat(),
                    'updatedAt': j.updated_at.isoformat()
                }
                for j in jobs
            ]
            return paginated_response(jobs_data, total, limit, offset)
        except ValueError:
            return error_response('Invalid pagination parameters', 400)
        except Exception as e:
            return error_response(f'Error fetching jobs: {str(e)}', 500)

    @app.route('/api/jobs/<int:job_id>', methods=['GET'])
    def get_job(job_id):
        job = Job.query.get(job_id)
        if not job:
            return error_response('Job not found', 404)
        return success_response({
            'id': job.id,
            'externalId': job.external_id,
            'source': job.source,
            'title': job.title,
            'company': job.company,
            'companyLogo': job.company_logo,
            'category': job.category,
            'rawCategory': job.raw_category,
            'jobType': job.job_type,
            'location': job.location,
            'salary': job.salary,
            'description': job.description,
            'fullDescription': job.full_description,
            'url': job.url,
            'applicationUrl': job.application_url,
            'applyUrl': job.apply_url,
            'tags': job.tags,
            'postedAt': job.posted_at.isoformat() if job.posted_at else None,
            'sourceName': job.source_name,
            'featured': job.featured,
            'postedByUserId': job.posted_by_user_id,
            'createdAt': job.created_at.isoformat(),
            'updatedAt': job.updated_at.isoformat()
        })

    @app.route('/api/jobs', methods=['POST'])
    @authenticate_token
    @authorize_role('employer', 'admin')
    def create_job():
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        company = data.get('company', '').strip()

        if not validate_string(title, min_length=3, max_length=255):
            return error_response('Job title must be 3-255 characters', 400)
        if not validate_string(company, min_length=1, max_length=255):
            return error_response('Company name required', 400)

        job = Job(
            source='internal',
            title=title,
            company=company,
            company_logo=data.get('companyLogo', '').strip() or None,
            category=data.get('category', '').strip() or None,
            job_type=data.get('jobType', '').strip() or None,
            location=data.get('location', '').strip() or None,
            salary=data.get('salary', '').strip() or None,
            description=data.get('description', '').strip() or None,
            full_description=data.get('fullDescription', '').strip() or None,
            url=data.get('url', '').strip() or None,
            tags=serialize_tags(data.get('tags')),
            source_name='HireFlow',
            featured=bool(data.get('featured', False)),
            posted_by_user_id=request.user.get('id')
        )
        db.session.add(job)
        db.session.commit()
        return success_response({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'createdAt': job.created_at.isoformat()
        }, 'Job posted successfully', 201)

    @app.route('/api/jobs/<int:job_id>', methods=['PUT'])
    @authenticate_token
    def update_job(job_id):
        job = Job.query.get(job_id)
        if not job:
            return error_response('Job not found', 404)
        if job.posted_by_user_id != request.user.get('id') and request.user.get('role') != 'admin':
            return error_response('Insufficient permissions', 403)

        data = request.get_json() or {}
        if 'title' in data:
            title = data['title'].strip()
            if not validate_string(title, min_length=3, max_length=255):
                return error_response('Job title must be 3-255 characters', 400)
            job.title = title
        if 'description' in data:
            job.description = data['description'].strip() or None
        if 'fullDescription' in data:
            job.full_description = data['fullDescription'].strip() or None
        if 'salary' in data:
            job.salary = data['salary'].strip() or None
        if 'location' in data:
            job.location = data['location'].strip() or None
        if 'tags' in data:
            job.tags = serialize_tags(data['tags'])
        if 'featured' in data:
            job.featured = bool(data['featured'])

        db.session.commit()
        return success_response(None, 'Job updated successfully')

    @app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
    @authenticate_token
    def delete_job(job_id):
        job = Job.query.get(job_id)
        if not job:
            return error_response('Job not found', 404)
        if job.posted_by_user_id != request.user.get('id') and request.user.get('role') != 'admin':
            return error_response('Insufficient permissions', 403)

        db.session.delete(job)
        db.session.commit()
        return success_response(None, 'Job deleted successfully')
