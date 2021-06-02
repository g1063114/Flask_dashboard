from flask import Blueprint

bp = Blueprint('main',__name__,url_prefix='/')

@bp.route('/')
def start_app():
    return 'start test'