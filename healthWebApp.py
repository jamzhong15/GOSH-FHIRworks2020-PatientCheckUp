from flask import Flask, render_template, url_for, redirect, request
from fhir_parser import FHIR, Patient, Observation
from forms import IdentifyForm, HeartRateForm, ChooseForm, BloodPressureForm
from access import Connect
from datetime import datetime
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "password"

fhir = FHIR("https://localhost:5001/api/", verify_ssl=False)

def search_patient(patientID):
  patient = fhir.get_patient(patientID)
  return patient.full_name()

@app.route("/", methods=["GET", "POST"])
def home():
  patient = None
  form = IdentifyForm()
  if form.validate_on_submit():
    patient_name = search_patient(form.patientID.data)
    return redirect(url_for("usr_page", name = patient_name))
  else:
    return render_template("home.html", title="form", form=form)

@app.route("/patient/<name>", methods=["POST", "GET"])
def usr_page(name):
  form  = ChooseForm()
  if request.method == "GET":
    return render_template("choose.html", url = name, form = form, name = name)
  elif form.validate_on_submit:
    if form.heartRate.data:
      return redirect(url_for("heart_rate", patient= name))
    elif form.bloodPressure.data:
      return redirect(url_for("blood_pressure", patient= name))


@app.route("/patient/<patient>/heartrate",methods=["POST", "GET"])
def heart_rate(patient):
  form = HeartRateForm()
  if request.method == "GET":
    return render_template("heartrate.html", title="form", form=form, name=patient)
  elif request.method == "POST":
    connect = Connect()
    result = connect.submit_heart_rate(patient, form.heartRate.data)
    time = result["date"]
    format_time = time[0:10] + " " + time[11:19]
    reading = str(result["heartrate"]) + "(BPM)"
    return render_template("submit.html", name=patient, time = format_time, reading = reading, type = "Heart Rate")

@app.route("/patient/<patient>/bloodpressure",methods=["POST", "GET"])
def blood_pressure(patient):
  form = BloodPressureForm()
  if request.method == "GET": 
    return render_template("bloodpressure.html", title="form", form=form, name=patient)
  elif request.method == "POST":
    connect = Connect()
    result = connect.submit_blood_pressure(patient, form.systolic.data, form.diastolic.data)
    time = result["date"]
    format_time = time[0:10] + " " + time[11:19]
    reading = "Systolic-" + str(result["systolic"]) + "Diastolic-" + str(result["diastolic"]) + "(mmHg)"

    return render_template("submit.html", name=patient, time = format_time, reading = reading, type = "Blood Pressure")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


if __name__ == "__main__":
  app.run(host="localhost", port=8000, debug=True)

