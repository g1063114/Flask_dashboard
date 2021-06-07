from flask import Blueprint, url_for, render_template, flash, request, session, g, send_file
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import os

from dashboard import db
from dashboard.models import User,File

from datetime import datetime

upload_path = 'C:\\projects\\Flask_dashboard\\dashboard\\upload'

bp = Blueprint('board',__name__,url_prefix='/board')

@bp.route('/link',methods=('GET','POST'))
def link():
    if g.user is None:
        return redirect(url_for('auth.login'))
    else:
        file_list = File.query.order_by(File.create_date.desc())
    return render_template('board/board.html',file_list=file_list)

@bp.route('/download',methods=('GET','POST'))
def download():
    if g.user is None:
        return redirect(url_for('auth.login'))
    return send_file('test.xlsx')

@bp.route('/upload',methods=('GET','POST'))
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename
        file_path = os.path.join(upload_path,file_name)
        file.save(file_path)
        file = File(name=file_name,path=file_path,create_date=datetime.now())
        db.session.add(file)
        db.session.commit()
        file_list = File.query.order_by(File.create_date.desc())
        return redirect(url_for('board.link'))

