from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()       # 전역으로 설정.  다른데서 가져오기 편함
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # config
    app.config.from_object(config)

    # db 설정
    db.init_app(app)
    migrate.init_app(app,db)

    # Blueprint
    from.views import main_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    
    return app