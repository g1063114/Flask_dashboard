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
nstu = pd.read_csv('C:\\projects\\Flask_dashboard\\dashboard\\data\\신입생충원현황.csv', encoding='cp949')
fail = pd.read_csv('C:\\projects\\Flask_dashboard\\dashboard\\data\\중도탈락현황.csv', encoding='cp949')
emp = pd.read_csv('C:\\projects\\Flask_dashboard\\dashboard\\data\\취업현황.csv', encoding='cp949')


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
    temp = pd.merge(nstu,emp, on=['info_yyyy','univ_id'],how ='inner').fillna(0)
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
    
    y_predict = mlr.predict(x_test)

    return jsonify(result = "success", result_data = predict_value[0][0])

@bp.route('/dash2',methods=['POST'])
def dash2():
    temp2 = pd.merge(nstu,emp, on=['info_yyyy','univ_id'],how ='inner').fillna(0)
    temp3 = pd.merge(temp2,pay, on=['info_yyyy','univ_id'],how ='inner').fillna(0)
    merge_data = pd.merge(temp3,fail, on=['info_yyyy','univ_id'],how ='inner').fillna(0)

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
    
    y_predict = mlr.predict(x_test)

    return jsonify(result = "success", result_data = predict_value[0][0])

@bp.route('/chart',methods=['POST'])
def chart():
    year = [2012,2013,2014,2015,2016,2017,2018,2019,2020]
    partici = list(nstu.groupby('info_yyyy').sum()['지원자'].values)
    max_enroll = list(nstu.groupby('info_yyyy').sum()['입학정원'].values)
    fail_values = list(fail.groupby('info_yyyy').sum()['중도탈락'].values)
    not_enroll = list(fail.groupby('info_yyyy').sum()['미등록'].values)
    not_back = list(fail.groupby('info_yyyy').sum()['미복학'].values)
    drop_out = list(fail.groupby('info_yyyy').sum()['자퇴'].values)
    
    # numpy 객체를 -> list 객체로 변환
    m_partici = list(map(lambda x:int(x),partici))
    m_max_enroll = list(map(lambda x:int(x),max_enroll))
    m_fail = list(map(lambda x:int(x),fail_values))
    m_not_enroll = list(map(lambda x:int(x),not_enroll))
    m_not_back = list(map(lambda x:int(x),not_back))
    m_drop_out = list(map(lambda x:int(x),drop_out))

    return jsonify(result="success", year=year, partici=m_partici, max_enroll=m_max_enroll, fail=m_fail, not_enroll=m_not_enroll, not_back=m_not_back, drop_out=m_drop_out)