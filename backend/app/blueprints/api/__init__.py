from flask import Blueprint
from .upload import upload_bp
from .model import model_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

# 注册子蓝图
api_bp.register_blueprint(upload_bp)
api_bp.register_blueprint(model_bp)

@api_bp.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    return response

@api_bp.errorhandler(404)
def handle_404(error):
    return {'error': 'API endpoint not found'}, 404

@api_bp.errorhandler(500)
def handle_500(error):
    return {'error': 'Internal server error'}, 500
