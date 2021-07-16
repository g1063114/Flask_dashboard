from flask import Blueprint, url_for, render_template, flash, request, session, g, send_file
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import os

from dashboard import db
from dashboard.models import User,File

from datetime import datetime

upload_path = 'C:\\projects\\Flask_dashboard\\dashboard\\upload\\'
ROW_PER_PAGE = 10

# 블루프린트 설정
# url_prefix 사용 예
# ex) /board/link , /board/download/1, /board/upload
bp = Blueprint('board',__name__,url_prefix='/board')

# 게시판 리스트
@bp.route('/link',methods=('GET','POST'))
def link():
    # 로그인 확인
    if g.user is None:
        return redirect(url_for('auth.login'))  # 로그인 안되어 있으면 로그인 페이지로 리다이렉트
    else:
        # 페이지 처리
        page = request.args.get('page', type=int, default=1)
        file_list = File.query.order_by(File.create_date.desc())    # 파일 리스트 정렬
        file_list = file_list.paginate(page, per_page=ROW_PER_PAGE) # 한 페이지에 10개씩 나오게 설정
        is_file = File.query.order_by(File.create_date.desc()).first()  # 파일 존재 유무 확인
        return render_template('board/board.html',file_list=file_list,is_file=is_file)

# 파일 다운로드
@bp.route('/download/<int:file>',methods=('GET','POST'))    # 쿼리 파라미터로 file id 넘겨줌
def download(file):
    if g.user is None:
        return redirect(url_for('auth.login'))  # 로그인 안되어 있으면 로그인 페이지로 리다이렉트
    else:
        down_file = File.query.filter_by(key=file).first()  # 쿼리 파라미터로 넘어온 file id 로 db에서 해당 파일 조회
        return send_file(down_file.path + down_file.name)   # send_file로 다운로드

# 파일 업로드
@bp.route('/upload',methods=('GET','POST'))
def upload():
    if g.user is None:
        return redirect(url_for('auth.login')) 
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename
        
        # 같은 이름의 파일 체크
        is_exist = File.query.filter_by(name=file_name).first()
        if is_exist != None:
            # 같은 파일 있으면 파일 이름에 현재 시간 정보 추가
            unique_time = datetime.now().strftime('%y%m%d_%H%M%S')          
            file_name = file_name.replace(".",f"_{unique_time}.")
        
        file_path = os.path.join(upload_path)
        file.save(file_path + file_name)    # 파일 저장

        # 파일 경로 db에 저장
        file = File(name=file_name,path=file_path,create_date=datetime.now())   # file 객체에 저장 = db 테이블에 저장 
        db.session.add(file)
        db.session.commit()
        return redirect(url_for('board.link'))

# 파일 삭제
@bp.route('/delete/<int:file>',methods=('GET','POST'))
def delete(file):
    if g.user is None:
        return redirect(url_for('auth.login'))
    else:
        # 파일 경로에서 파일 제거, db에서 파일 경로 제거
        delete_file = File.query.filter_by(key=file).first()
        os.remove(upload_path + delete_file.name)
        db.session.delete(delete_file)
        db.session.commit()
        return redirect(url_for('board.link'))
