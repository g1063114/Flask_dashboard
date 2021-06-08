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

    chart1(y_test,y_predict)

    return jsonify(result = "success", result_data = predict_value[0][0])

@bp.route('/chart',methods=['POST'])
def chart():
    partici = list(nstu.groupby('info_yyyy').sum()['지원자'].values)
    max_enroll = list(nstu.groupby('info_yyyy').sum()['입학정원'].values)
    print(partici)
    print(max_enroll)