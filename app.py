from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import traceback
import re
from datetime import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///report.db'
db = SQLAlchemy(app)

# Создание моделей таблиц баз данныых
class AddClient(db.Model):
    # __tablename__ = 'addclient'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    contact = db.Column(db.String(150), unique=True, nullable = False)

    def __repr__(self): 
        return '<Client %r>' % self.id

class Report(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.Integer(), db.ForeignKey('add_client.id'))
    service = db.Column(db.String(150), nullable = False)
    service_price = db.Column(db.Integer(), nullable = False)
    date = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return '<Service %r>' % self.id


@app.route('/')
def index():
    addclient = AddClient.query.all()
    reports = Report.query.all()
    return render_template("index.html", addclient=addclient, reports=reports)


@app.route('/create-report-clients', methods=['POST', 'GET'])
def create_report_clients():
    clients = AddClient.query.all()
    if request.method == 'POST':
        return render_template("create_report_clients.html", clients=clients)
    else:
        return render_template("create_report_clients.html")


@app.route('/create-report', methods=['POST', 'GET'])
def create_report():
    if request.method == 'POST':
        reports = Report.query.all()
        return render_template("create_report.html", reports=reports)
    else:
        return render_template("create_report.html")
    


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/addclient', methods=['POST', 'GET'])
def addclient():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']

        addclient = AddClient(name=name, contact=contact)
        try:
            db.session.add(addclient)
            db.session.commit()
            return redirect('/')
        except:
            return traceback.format_exc()

    else:
        return render_template("addclient.html")


@app.route('/report',  methods=['POST', 'GET'])
def report():
    clients = AddClient.query.all()
    if request.method == 'POST':
        client_id = request.form['client_id']
        service = request.form['service']
        service_price = request.form['service_price']

        date_str = request.form['date']
        date = dt.strptime(date_str, '%d.%m.%Y')

        report = Report(client_id=client_id, service=service, service_price=service_price, date=date)

        try:
            db.session.add(report)
            db.session.commit()
            return redirect('/')
        except:
            return traceback.format_exc()
        pass
    else:
        return render_template("report.html", clients=clients)
    


if __name__ == "__main__":
    app.run(debug=True)


