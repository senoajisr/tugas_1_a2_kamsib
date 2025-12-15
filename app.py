from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.secret_key = "secret123"

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

# Model database
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    grade = db.Column(db.String(10))

# Decorator login
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated

# Route LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin":
            session['logged_in'] = True
            return redirect('/home')
        else:
            return render_template('login.html', error="Username/Password salah!")

    return render_template('login.html')

# HOME
@app.route('/home')
@login_required
def home():
    students = Student.query.all()
    return render_template('home.html', students=students)

# ADD STUDENT
@app.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form['name']
    age = int(request.form['age'])
    grade = request.form['grade']

    new_student = Student(name=name, age=age, grade=grade)
    db.session.add(new_student)
    db.session.commit()
    return redirect('/home')

# EDIT STUDENT
@app.route('/edit/<int:id>')
@login_required
def edit(id):
    student = Student.query.get(id)
    if not student:
        return redirect('/home')
    return render_template('edit.html', student=student)

# UPDATE STUDENT
@app.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    student = Student.query.get(id)
    if not student:
        return redirect('/home')

    student.name = request.form['name']
    student.age = int(request.form['age'])
    student.grade = request.form['grade']
    db.session.commit()
    return redirect('/home')

# DELETE STUDENT
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
    return redirect('/home')

# LOGOUT
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
