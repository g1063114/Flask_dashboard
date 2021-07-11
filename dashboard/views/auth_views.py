from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from dashboard import db
from dashboard.forms import UserCreateForm, UserLoginForm, UserResetPasswordForm
from dashboard.models import User

from datetime import datetime

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/signup/',methods=('GET','POST'))
def signup():
    # form 객체 생성
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            # db에 user 가 없으면 저장 
            # 비밀번호는 hash 암호화 적용해서 저장
            user = User(userid=form.userid.data, password=generate_password_hash(form.password1.data),
                        email=form.email.data, univ=form.univ.data, dept=form.dept.data, create_date=datetime.now())
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.start_app'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html',form=form)

@bp.route('/login/',methods=('GET','POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password,form.password.data):
            error = '비밀번호가 일치하지 않습니다.'
        if error is None:
            # 세션에 유저 정보 저장
            session.clear()
            session['user_id'] = user.key
            return redirect(url_for('main.start_app'))
        flash(error)
    return render_template('auth/login.html',form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.start_app'))

@bp.before_app_request
def get_login_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/reset/',methods=('GET','POST'))
def reset():
    form = UserResetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            error = '존재하지 않는 사용자입니다.'
        else:
            # 사용자가 존재하는지만 체크 
            # 비밀번호는 암호화 해서 저장했기 때문에 비교 불가 따라서 비밀번호 새로 저장
            user.password = generate_password_hash(form.password.data)
            db.session.commit()
            return redirect(url_for('main.start_app'))
        flash(error)
    return render_template('auth/reset.html',form=form)

