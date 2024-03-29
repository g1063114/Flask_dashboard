from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()       # 전역으로 설정.  다른데서 가져오기 편함
migrate = Migrate()

# 페이지 요청 잘못했을 때 보여지는 화면
def page_not_found(e):
    return render_template('404.html'),404

# url 요청하면 처음으로 들어오는 곳
# Flask 객체를 만들어서 config 파일 설정하고 db 설정하고
# url 경로 매핑을 쉽게 하기 위해서 blueprint 사용해서 HTTP API 구현

def create_app():
    app = Flask(__name__)
    
    # config
    app.config.from_envvar('APP_CONFIG_FILE')

    # db 설정
    db.init_app(app)
    migrate.init_app(app,db)

    # Blueprint
    from.views import main_views, auth_views, board_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(board_views.bp)

    # filter
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # 404 오류 페이지
    app.register_error_handler(404, page_not_found)
    
    return app