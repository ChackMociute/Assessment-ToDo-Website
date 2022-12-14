from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from datetime import date

# Returns function pointer for validating string length in a flask form
def length_check(length=50):
    def _length_check(form, field):
        if len(field.data) > length:
            raise ValidationError(f"Entry mustn't exceed {length} characters")
    return _length_check

# Validator for ensuring due date hasn't passed
def date_check(form, field):
    if field.data < date.today():
        raise ValidationError("Due date should not be in the past")

class AssessmentForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), length_check()])
    code = StringField('title', validators=[DataRequired(), length_check(20)])
    deadline = DateField('deadline', format='%Y-%m-%d', validators=[DataRequired(), date_check])
    description = TextAreaField('description', validators=[DataRequired(), length_check(1000)])