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

@bp.route('/export')
def export():
    return send_file('test.xlsx')

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

    return jsonify(result = "success", result_data = format(m_predict_value[0],".3f"))

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

    return jsonify(result = "success", result_data = format(m_predict_value[0],".3f"))

@bp.route('/chart',methods=['POST'])
def chart():
    year = [2012,2013,2014,2015,2016,2017,2018,2019,2020]

    partici = list(student.groupby('info_yyyy').sum()['지원자'].values)
    max_enroll = list(student.groupby('info_yyyy').sum()['입학정원'].values)

    drop_out_values = list(drop_out.groupby('info_yyyy').sum()['중도탈락'].values)
    not_enroll = list(drop_out.groupby('info_yyyy').sum()['미등록'].values)
    not_back = list(drop_out.groupby('info_yyyy').sum()['미복학'].values)
    leave = list(drop_out.groupby('info_yyyy').sum()['자퇴'].values)

    # occasional = list(enter_type.groupby('info_yyyy').sum()['수시'].values)
    # regular = list(enter_type.groupby('info_yyyy').sum()['정시'].values)
    # additional = list(enter_type.groupby('info_yyyy').sum()['추가'].values)
    # final = list(enter_type.sum()['최종'].values)
    
    # print(occasional)
    
    # numpy 객체를 -> list 객체로 변환
    m_partici = list(map(lambda x:int(x),partici))
    m_max_enroll = list(map(lambda x:int(x),max_enroll))
    m_drop_out_total = list(map(lambda x:int(x),drop_out_values))
    m_not_enroll = list(map(lambda x:int(x),not_enroll))
    m_not_back = list(map(lambda x:int(x),not_back))
    m_drop_out = list(map(lambda x:int(x),leave))

    return jsonify(result="success", year=year, partici=m_partici, max_enroll=m_max_enroll, drop_out_total=m_drop_out_total, not_enroll=m_not_enroll, not_back=m_not_back, drop_out=m_drop_out)