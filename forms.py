from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class IdentifyForm(FlaskForm):
    patientID = StringField('Patient ID*')
    next = SubmitField('Verify')

class ChooseForm(FlaskForm):
    heartRate = SubmitField('Log Heart Rate')
    bloodPressure = SubmitField('Log Blood Pressure')
    back = SubmitField('Back')

class HeartRateForm(FlaskForm):
    heartRate = StringField('Heart Rate (BPM)')
    submit= SubmitField('Submit')

class BloodPressureForm(FlaskForm):
    systolic = StringField('Systolic Reading (mmHg)')
    diastolic = StringField('Diastolic Reading (mmHg)')
    submit = SubmitField('Submit')


