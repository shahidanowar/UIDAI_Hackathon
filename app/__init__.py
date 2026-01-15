"""
Flask Application Factory
"""

from flask import Flask
from flask_cors import CORS
from app.extensions import db
from app.config import Config


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.analysis import analysis_bp
    from app.routes.prediction import prediction_bp
    from app.routes.policies import policies_bp
    from app.routes.todo import todo_bp
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
    app.register_blueprint(prediction_bp, url_prefix='/prediction')
    app.register_blueprint(policies_bp, url_prefix='/policies')
    app.register_blueprint(todo_bp, url_prefix='/todo')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
