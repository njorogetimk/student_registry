from flask import Blueprint, request, render_template, url_for, redirect

from src.models import Student, db

stud = Blueprint('stud', __name__, url_prefix='/stud/v1/')





@stud.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


@stud.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)

@stud.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = request.form['age']
        bio = request.form['bio']

        student = Student(firstname=firstname, lastname=lastname, email=email, age=age, bio=bio)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('stud.index'))
    return render_template('create.html')


@stud.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = request.form['age']
        bio = request.form['bio']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('stud.student', student_id=student.id))
    
    return render_template('edit.html', student=student)


@stud.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('stud.index'))