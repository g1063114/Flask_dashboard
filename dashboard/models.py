from dashboard import db

# DB에 저장될 테이블, 객체
# db User table
class User(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    univ = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(120), nullable=False)
    create_date = db.Column(db.DateTime(),nullable=False)

# db File table
class File(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300),nullable=False)
    path = db.Column(db.String(200),nullable=False)
    create_date = db.Column(db.DateTime(),nullable=False)