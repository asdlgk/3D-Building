from flask import Flask
from .config import DevelopmentConfig, ProductionConfig
from .extensions import db, socketio, cors, make_celery

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # 配置加载
    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # 插件初始化
    db.init_app(app)
    cors.init_app(app)
    socketio.init_app(app)
    
    # 注册蓝图
    from .blueprints.api import bp as api_bp
    from .blueprints.ws import bp as ws_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(ws_bp)
    
    # 确保上传目录存在
    with app.app_context():
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            os.makedirs(folder, exist_ok=True)
    
    return app

# 创建Celery实例
celery = make_celery(create_app())
