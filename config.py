import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR,'dashboard.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'temp'     # 테스트용도로 설정 -> 운영으로 배포할 때 변경해야함