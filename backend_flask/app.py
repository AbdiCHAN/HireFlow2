import os
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge

from .extensions import db
from .routes.admin import admin_bp
from .routes.api_keys import api_keys_bp
from .routes.applications import applications_bp
from .routes.auth import auth_bp
from .routes.cv import cv_bp
from .routes.jobs import jobs_bp


def load_dotenv_if_available():
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def register_cors(app):
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return "", 204
        return None

    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin") or "*"
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return response


def register_error_handlers(app):
    @app.errorhandler(RequestEntityTooLarge)
    def payload_too_large(_error):
        return jsonify({"error": "File too large"}), 413

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Not found"}), 404
        return error


def register_frontend_static(app):
    dist_path = Path(app.config["ROOT_DIR"]) / "dist"
    if not dist_path.exists():
        return

    @app.get("/")
    @app.get("/<path:path>")
    def serve_frontend(path=""):
        if path.startswith("api/"):
            abort(404)

        candidate = dist_path / path
        if path and candidate.exists() and candidate.is_file():
            return send_from_directory(dist_path, path)
        return send_from_directory(dist_path, "index.html")


def create_app(test_config=None):
    load_dotenv_if_available()
    from .config import Config

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if database_uri.startswith("sqlite:///") and database_uri != "sqlite:///:memory:":
        Path(database_uri.replace("sqlite:///", "", 1)).parent.mkdir(parents=True, exist_ok=True)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    register_cors(app)
    register_error_handlers(app)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(cv_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_keys_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    with app.app_context():
        db.create_all()

    register_frontend_static(app)
    return app


def main():
    app = create_app()
    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
