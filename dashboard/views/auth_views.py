from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from dashboard import db
from dashboard.forms import UserCreateForm
from dashboard.models import User

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/signup/',methods=('GET','POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            user = User(userid=form.userid.data, password=generate_password_hash(form.password1.data),
                        email=form.email.data, univ=form.univ.data, dept=form.dept.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.start_app'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html',form=form)
