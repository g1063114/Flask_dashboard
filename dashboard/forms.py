from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp

class UserCreateForm(FlaskForm):
    userid = StringField('사용자아이디',validators=[DataRequired('아이디 입력은 필수 항목입니다.'),Length(min=3,max=25)])
    password1 = PasswordField('비밀번호',validators=[DataRequired('비밀번호 입력은 필수 항목입니다.'),EqualTo('password2','비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인',validators=[DataRequired('비밀번호 확인 입력은 필수 항목입니다.')])
    email = EmailField('이메일',validators=[DataRequired('이메일 입력은 필수 항목입니다.'),Email()])
    univ = StringField('소속 대학교',validators=[DataRequired('소속 대학교 입력은 필수 항목입니다.'),Length(min=3,max=20)])
    dept = StringField('소속 부서',validators=[DataRequired('소속 부서 입력은 필수 항목입니다.')])