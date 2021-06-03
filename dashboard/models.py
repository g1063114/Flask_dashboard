from dashboard import db

class User(db.Model):
    key = db.Columm(db.Integer, primary_key=True)
    userid = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    univ = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(120), nullable=False)