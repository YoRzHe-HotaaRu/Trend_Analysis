from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from datetime import datetime
import os

# Import API routes
from api.routes.transit_routes import transit_bp
from api.routes.attraction_routes import attraction_bp
from api.routes.analysis_routes import analysis_bp
from api.routes.dashboard_routes import dashboard_bp

# Import external API services
from external_apis.grab_api import GrabAPIService
from external_apis.google_places import GooglePlacesService
from external_apis.foursquare_api import FoursquareService
from external_apis.osm_api import OpenStreetMapService

# Import database and caching
from models.database import db, init_db
from utils.data_cache import cache_manager

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'klang-valley-transit-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///klang_valley.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Enable CORS for React frontend
CORS(app, origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.environ.get('FRONTEND_URL', 'http://localhost:3000')
])

# Initialize database
db.init_app(app)
with app.app_context():
    init_db()

# Register API blueprints
app.register_blueprint(transit_bp, url_prefix='/api/transit')
app.register_blueprint(attraction_bp, url_prefix='/api/attractions')
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Root endpoint
@app.route('/')
def root():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Klang Valley Transit & Attractions API',
        'version': '1.0.0',
        'endpoints': {
            'transit': '/api/transit',
            'attractions': '/api/attractions',
            'analysis': '/api/analysis',
            'dashboard': '/api/dashboard',
            'health': '/health'
        },
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# Request logging middleware
@app.before_request
def log_request():
    app.logger.info(f"{request.method} {request.path} - {request.remote_addr}")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    # Development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )