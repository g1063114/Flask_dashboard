from flask import Blueprint, send_file, render_template

bp = Blueprint('main',__name__,url_prefix='/')

@bp.route('/')
def start_app():
    return render_template('index/index.html')

@bp.route('/export')
def export():
    return send_file('test.xlsx')