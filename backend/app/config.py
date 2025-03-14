import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
    OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'static/outputs')
    
    # 算法服务配置
    AUTODL_HOST = os.getenv('AUTODL_HOST', 'gpu-server.example.com')
    SSH_KEY_PATH = os.getenv('SSH_KEY_PATH', '/home/user/.ssh/id_rsa')
    
    # Celery配置
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///temp.db'
