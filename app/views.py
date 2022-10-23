from flask import render_template, flash, redirect, url_for, request
from app import app, db
from .models import Assessment
from .forms import AssessmentForm, ParameterForm

def complete(list):
    for id in list:
        Assessment.query.get(int(id)).complete = True

def uncomplete(list):
    for id in list:
        Assessment.query.get(int(id)).complete = False

def delete(list):
    for id in list:
        db.session.delete(Assessment.query.get(int(id)))

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ParameterForm()

    if 'home_button' in request.form:
        globals()[request.form['home_button']](request.form.getlist('assessment_id'))
        db.session.commit()
        return redirect(url_for('home'))
    if 'show_button' in request.form:
        return redirect(url_for('home'))
    return render_template('home.html', assessments=Assessment.query.all(), form=form)

@app.route('/add', methods=['GET', 'POST'])
def add_new():
    form = AssessmentForm()
    if form.validate_on_submit():
        db.session.add(Assessment(
            title=form.title.data,
            code=form.code.data,
            deadline = form.deadline.data,
            description = form.description.data,
            complete = False
        ))
        db.session.commit()
        flash('Assessment added successfully')
        return redirect(url_for('add_new'))
    return render_template('add.html', title='Add new', form=form)

@app.route('/completed', methods=['GET', 'POST'])
def completed():
    return render_template('complete.html', assessments=[x for x in Assessment.query.all() if x.complete])

@app.route('/incomplete', methods=['GET', 'POST'])
def incomplete():
    return render_template('incomplete.html', assessments=[x for x in Assessment.query.all() if not x.complete])