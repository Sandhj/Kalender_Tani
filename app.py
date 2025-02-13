from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model database untuk tugas
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    color = db.Column(db.String(20), nullable=False)

# Sinkronisasi database
with app.app_context():
    db.create_all()

# Halaman utama
@app.route('/')
def index():
    current_year = datetime.now().year
    tasks = Task.query.all()
    return render_template('index.html', year=current_year, tasks=tasks)

# API untuk menambahkan tugas manual
@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    date = request.form['date']
    color = request.form.get('color', '#FF0000')  # Default warna merah

    new_task = Task(title=title, date=datetime.strptime(date, '%Y-%m-%d').date(), color=color)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

# API untuk menambahkan tugas otomatis
@app.route('/add_task_auto', methods=['POST'])
def add_task_auto():
    title = request.form['title']
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
    interval = int(request.form['interval'])
    duration_months = int(request.form['duration_months'])
    color = request.form.get('color', '#0000FF')  # Default warna biru

    end_date = start_date + timedelta(days=30 * duration_months)

    current_date = start_date
    while current_date <= end_date:
        new_task = Task(title=title, date=current_date, color=color)
        db.session.add(new_task)
        current_date += timedelta(days=interval)

    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5009)
