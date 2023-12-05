from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import traceback
import sys
from werkzeug.security import generate_password_hash, check_password_hash
import os
import numpy as np
from mysqlquerys import connect
from mysqlquerys import mysql_rm
from cheltuieli import chelt_plan
from cheltuieli.chelt_plan import CheltuieliPlanificate, Income
from cheltuieli.masina import Masina

app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret"

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'


class Users(UserMixin):
    def __init__(self, user_name):
        self.name = user_name
        self.id = None


@login_manager.user_loader
def load_user(user_id):
    print(sys._getframe().f_code.co_name, request.method)
    print(20*'##')
    print('user_id', user_id)
    print(20*'##')
    user = Users(user_id)
    return user


@app.route('/', methods=['GET', 'POST'])
def index():
    # print(sys._getframe().f_code.co_name, request.method)
    print('++++', request.method)
    # iniFile = None
    # form = iniFileCls()
    # if form.validate_on_submit():
    #     iniFile = form.iniFile.data
    #     # ttt = UPLOAD_PATH
    #     # print(iniFile)
    #     # print(UPLOAD_PATH)
    #     form.iniFile.data = ''
    # if request.method == 'POST':
    #     username = request.form['username']
    #     email = request.form['email']
    #     cur = mysql.connection.cursor()
    #     cur.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (username, email))
    #     mysql.connection.commit()
    #     cur.close()
    # cur = mysql.connection.cursor()
    # users = cur.execute('SELECT * FROM aeroclub')
    # ini_file = r"D:\Python\MySQL\web_db.ini"
    # data_base_name = 'heroku_6ed6d828b97b626'
    # app = QApplication([])
    # iniFile, a = QFileDialog.getOpenFileName(None, 'Open data base configuration file', '',
    #                                          "data base config files (*.ini)")
    # dataBase = connect.DataBase(ini_file, data_base_name)
    # tableHead = ['name', 'value', 'myconto', 'freq', 'pay_day', 'valid_from', 'valid_to', 'auto_ext', 'post_pay']
    # all_chelt = []
    # for table in dataBase.tables:
    #     dataBase.active_table = table
    #     check = all(item in list(dataBase.active_table.columnsProperties.keys()) for item in tableHead)
    #     if check:
    #         vals = dataBase.active_table.returnColumns(tableHead)
    #         for row in vals:
    #             row = list(row)
    #             row.insert(0, table)
    #             all_chelt.append(row)
    #
    # newTableHead = ['table']
    # for col in tableHead:
    #     newTableHead.append(col)
    # params = config(iniFile)
    # print(params)
    # if users > 0:
    #     userDetails = cur.fetchall()
    # userDetails = {'ddd': 'ggg'}
    # user = os.environ.get('USERNAME')
    # user = os.getlogin()
    user = 'user'
    conf = connect.Config('static/wdb.ini')
    users_table = mysql_rm.Table(conf.credentials, 'users')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        matches = ('username', username)
        hashed_pass = users_table.returnCellsWhere('password', matches)
        if check_password_hash(hashed_pass[0], password):
            user = Users('aa')
            login_user(user)
            print(user.is_authenticated)
            # return redirect(url_for('cheltuieli'))
        else:
            print('BOOOOO')
    return render_template('index.html', iniFile=user, current_user=user)#, userDetails='all_chelt', database_name='heroku_6ed6d828b97b626'


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # print(sys._getframe().f_code.co_name, request.method)
    conf = connect.Config('static/wdb.ini')
    users_table = mysql_rm.Table(conf.credentials, 'users')
    # users = users_table.returnAllRecordsFromTable()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cols = ('username', 'email', 'password')
        hash = generate_password_hash(password)
        vals = (username, email, hash)
        users_table.addNewRow(cols, vals)
    elif request.method == 'GET':
        print('****', request.method)

    return render_template('register.html')


@app.route('/cheltuieli', methods=['GET', 'POST'])
@login_required
def cheltuieli():
    chelt_app = CheltuieliPlanificate('static/wdb.ini')
    income_app = Income('static/wdb.ini')
    # chelt_app = CheltuieliPlanificate('static/heroku.ini')
    dataFrom, dataBis = chelt_plan.default_interval()
    conto = 'all'

    if request.method == 'POST':
        month = request.form['month']
        year = int(request.form['year'])
        conto = request.form['conto']
        dataFrom = request.form['dataFrom']
        dataBis = request.form['dataBis']
        if month != 'interval':
            dataFrom, dataBis = chelt_plan.get_monthly_interval(month, year)
        elif month == 'interval' and (dataFrom == '' or dataBis == ''):
            dataFrom, dataBis = chelt_plan.default_interval()
        else:
            try:
                dataFrom = datetime.strptime(dataFrom, "%Y-%m-%d")
                dataBis = datetime.strptime(dataBis, "%Y-%m-%d")
                print(dataFrom.date(), dataBis.date())
            except:
                print(traceback.format_exc())
    try:
        if isinstance(dataFrom, datetime):
            chelt_app.prepareTablePlan(conto, dataFrom.date(), dataBis.date())
            income_app.prepareTablePlan(conto, dataFrom.date(), dataBis.date())
        elif isinstance(dataFrom, date):
            chelt_app.prepareTablePlan(conto, dataFrom, dataBis)
            income_app.prepareTablePlan(conto, dataFrom, dataBis)
    except:
        print(traceback.format_exc())

    return render_template('cheltuieli.html',
                           expenses=chelt_app.expenses,
                           income=income_app.income,
                           total_netto=income_app.netto,
                           total_taxes=income_app.taxes,
                           total_brutto=income_app.brutto,
                           salary_uberweisung=income_app.salary_uberweisung,
                           salary_abzuge=income_app.salary_abzuge,
                           salary_netto=income_app.salary_netto,
                           salary_gesetzliche_abzuge=income_app.salary_gesetzliche_abzuge,
                           salary_brutto=income_app.salary_brutto,
                           tot_no_of_monthly_expenses=chelt_app.tot_no_of_monthly_expenses(),
                           tot_val_of_monthly_expenses=chelt_app.tot_val_of_monthly_expenses(),
                           tot_no_of_irregular_expenses=chelt_app.tot_no_of_irregular_expenses(),
                           tot_val_of_irregular_expenses=chelt_app.tot_val_of_irregular_expenses(),
                           tot_no_of_expenses=chelt_app.tot_no_of_expenses(),
                           tot_val_of_expenses=chelt_app.tot_val_of_expenses(),
                           tot_no_of_income='chelt_app.tot_no_of_income()',
                           tot_val_of_income='chelt_app.tot_val_of_income()',
                           dataFrom=dataFrom,
                           dataBis=dataBis
                           )


@app.route('/masina', methods=['GET', 'POST'])
def masina():
    print(sys._getframe().f_code.co_name, request.method)
    app_masina = Masina('static/wdb.ini')
    dataFrom, dataBis = app_masina.default_interval
    alim_type = None
    if request.method == 'POST':
        print(request.method)
        if "submit_request" in request.form:
            month = request.form['month']
            alim_type = request.form['type']
            if alim_type == 'all':
                alim_type = None
            dataFrom = request.form['dataFrom']
            dataBis = request.form['dataBis']
            if month != 'interval':
                dataFrom, dataBis = app_masina.get_monthly_interval(month)
            elif month == 'interval' and (dataFrom == '' or dataBis == ''):
                dataFrom, dataBis = app_masina.default_interval
            else:
                try:
                    dataFrom = datetime.strptime(dataFrom, "%Y-%m-%d")
                    dataBis = datetime.strptime(dataBis, "%Y-%m-%d")
                except:
                    print(traceback.format_exc())
        elif "add_alim" in request.form:
            print("add_alim")
            date = request.form['data']
            alim_type = request.form['type']
            brutto = request.form['brutto']
            amount = request.form['amount']
            km = request.form['km']

            ppu = round(float(brutto)/float(amount), 3)
            columns = ['data', 'type', 'brutto', 'amount', 'ppu', 'km']
            values = [date, alim_type, brutto, amount, ppu, km]
            app_masina.insert_new_alim(columns, values)
        else:
            print("AAAA")

    alimentari = app_masina.get_alimentari_for_interval_type(dataFrom, dataBis, alim_type)
    return render_template('masina.html',
                           userDetails=alimentari,
                           total=app_masina.total_money,
                           tot_el=app_masina.tot_electric,
                           tot_benz=app_masina.tot_benzina,
                           dataFrom=dataFrom.date(),
                           dataBis=dataBis.date(),
                           # tot_lm=tot_lm,
                           # lm_benz=lm_benz,
                           # lm_elec=lm_elec,
                           # date_from=date_from.date()
                           )


if __name__ == "__main__":
    app.run(debug=True)
