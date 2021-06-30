from flask import Blueprint, send_file, render_template, request,jsonify, Response
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

bp = Blueprint('main',__name__,url_prefix='/')

pay = pd.read_csv('C:\\projects\\Flask_dashboard\\dashboard\\data\\등록금현황.csv', encoding='cp949')
student = pd.read_csv('C:\\projects\\Flask_dashboard\\dashboard\\data\\신입생충원현황.csv', encoding='cp949')
drop_out = pd.read_csv('C:\\projects\\Flask_dashboard\\dashboard\\data\\중도탈락현황.csv', encoding='cp949')
job = pd.read_csv('C:\\projects\\Flask_dashboard\\dashboard\\data\\취업현황.csv', encoding='cp949')
enter_type = pd.read_csv('C:\\projects\\Flask_dashboard\\dashboard\\data\\입학유형현황.csv', encoding='cp949')

@bp.route('/')
def start_app():
    return render_template('base.html')

@bp.route('/index')
def main_app():
    return render_template('main.html')

@bp.route('/dash1',methods=['POST'])
def dash1():
    temp = pd.merge(student,job, on=['info_yyyy','univ_id'],how ='inner').fillna(0)
    merge_data = pd.merge(temp,pay, on=['info_yyyy','univ_id'],how ='inner').fillna(0)

    recruit = request.form['recruit']
    employ = request.form['emp']
    payment = request.form['payment']

    x = merge_data[['모집인원','연계취업자','등록금']]
    y = merge_data[['지원자']]

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2)

    mlr = LinearRegression() 
    mlr.fit(x_train, y_train) 

    insert_data = [[recruit,employ,payment]]
    predict_value = mlr.predict(insert_data)
    m_predict_value = list(map(lambda x:float(x),predict_value))

    y_predict = mlr.predict(x_test)
    score = mlr.score(x_train,y_train)

    return jsonify(result = "success", result_data = format(m_predict_value[0],".3f"), score=format(score,".3f"))

@bp.route('/dash2',methods=['POST'])
def dash2():
    temp2 = pd.merge(student,job, on=['info_yyyy','univ_id'],how ='inner').fillna(0)
    temp3 = pd.merge(temp2,pay, on=['info_yyyy','univ_id'],how ='inner').fillna(0)
    merge_data = pd.merge(temp3,drop_out, on=['info_yyyy','univ_id'],how ='inner').fillna(0)

    recruit = request.form['recruit']
    employ = request.form['emp']
    payment = request.form['payment']
    parti = request.form['partici']

    x = merge_data[['연계취업자','지원자','모집인원','등록금']]
    y = merge_data[['중도탈락']]

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2)

    mlr = LinearRegression() 
    mlr.fit(x_train, y_train) 

    insert_data = [[employ,parti,recruit,payment]]
    predict_value = mlr.predict(insert_data)
    m_predict_value = list(map(lambda x:float(x),predict_value))
 
    y_predict = mlr.predict(x_test)
    score = mlr.score(x_train,y_train)

    return jsonify(result = "success", result_data = format(m_predict_value[0],".3f"), score=format(score,".3f"))

@bp.route('/chart',methods=['POST'])
def chart():
    year = [2012,2013,2014,2015,2016,2017,2018,2019,2020]
    year_3 = [2018,2019,2020]

    partici = list(student.groupby('info_yyyy').sum()['지원자'].values)
    max_enroll = list(student.groupby('info_yyyy').sum()['입학정원'].values)

    drop_out_values = list(drop_out.groupby('info_yyyy').sum()['중도탈락'].values)
    not_enroll = list(drop_out.groupby('info_yyyy').sum()['미등록'].values)
    not_back = list(drop_out.groupby('info_yyyy').sum()['미복학'].values)
    leave = list(drop_out.groupby('info_yyyy').sum()['자퇴'].values)

    job_emp = list(job.groupby('info_yyyy').sum()['연계취업자'].values)
    job_overseas = list(job.groupby('info_yyyy').sum()['해외취업자'].values)
    job_study = list(job.groupby('info_yyyy').sum()['진학자'].values)

    # 3개년 입학 유형
    temp = enter_type.groupby(['info_yyyy','jh_type']).sum()
    temp['합계'] = temp['수시등록'] +temp['정시등록']+temp['추가등록']
    signin = pd.pivot_table(temp,index='jh_type', columns='info_yyyy',values=['합계'], aggfunc='sum')
    
    signin_1 = list(signin['합계'].iloc[:,0].values)
    signin_2 = list(signin['합계'].iloc[:,1].values)
    signin_3 = list(signin['합계'].iloc[:,2].values)

    label_temp = list(enter_type['jh_type'].drop_duplicates())
    signin_label = sorted(label_temp)

    # numpy 객체 값을 -> int,str list로 변환
    m_partici = list(map(lambda x:int(x),partici))
    m_max_enroll = list(map(lambda x:int(x),max_enroll))
    m_drop_out_total = list(map(lambda x:int(x),drop_out_values))
    m_not_enroll = list(map(lambda x:int(x),not_enroll))
    m_not_back = list(map(lambda x:int(x),not_back))
    m_drop_out = list(map(lambda x:int(x),leave))
    m_signin_1 = list(map(lambda x:str(x),signin_1))
    m_signin_2 = list(map(lambda x:str(x),signin_2))
    m_signin_3 = list(map(lambda x:str(x),signin_3))
    m_job_emp = list(map(lambda x:int(x),job_emp))
    m_job_overseas = list(map(lambda x:int(x),job_overseas))
    m_job_study = list(map(lambda x:int(x),job_study))

    return jsonify(result="success", year=year, partici=m_partici, max_enroll=m_max_enroll, drop_out_total=m_drop_out_total, 
                    not_enroll=m_not_enroll, not_back=m_not_back, drop_out=m_drop_out,
                    signin_1=m_signin_1, signin_2=m_signin_2,signin_3=m_signin_3, year3=year_3, signin_label=signin_label,
                    job_emp=m_job_emp, job_overseas=m_job_overseas,job_study=m_job_study)