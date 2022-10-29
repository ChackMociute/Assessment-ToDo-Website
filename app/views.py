from flask import render_template, flash, redirect, url_for, request
from app import app, db
from .models import Assessment
from .forms import AssessmentForm

def mark_complete(id):
    Assessment.query.get(int(id)).complete = True

def mark_uncomplete(id):
    Assessment.query.get(int(id)).complete = False

def delete(id):
    db.session.delete(Assessment.query.get(int(id)))

def button_pressed(button):
    return button in request.form

def modify_selected(func_name):
    for id in request.form.getlist('assessment_id'):
        globals()[func_name](id)
    db.session.commit()

def base(page, assessments):
    if button_pressed(f'{page}_button'):
        modify_selected(request.form[f'{page}_button']) # Button value corresponds to function name
        return redirect(url_for(page))
    return render_template(f'{page}.html', assessments=assessments)

def collect_assessments(complete=True, incomplete=True):
    return sorted([ass for ass in Assessment.query.all()
                   if ass.complete == complete
                   or ass.complete != incomplete], key=lambda x: x.deadline)

@app.route('/', methods=['GET', 'POST'])
def home():
    return base('home', collect_assessments())

@app.route('/complete', methods=['GET', 'POST'])
def complete():
    return base('complete', collect_assessments(incomplete=False))

@app.route('/incomplete', methods=['GET', 'POST'])
def incomplete():
    return base('incomplete', collect_assessments(complete=False))

def add_assessment(form):
    db.session.add(Assessment(
        title=form.title.data,
        code=form.code.data,
        deadline = form.deadline.data,
        description = form.description.data,
        complete = False
    ))
    db.session.commit()
    flash('Assessment added successfully')

@app.route('/add', methods=['GET', 'POST'])
def add_new():
    form = AssessmentForm()
    if form.validate_on_submit():
        add_assessment(form)
        return redirect(url_for('add_new'))
    return render_template('add.html', title='Add new', form=form)