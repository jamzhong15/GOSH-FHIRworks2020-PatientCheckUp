import requests
import json
from datetime import datetime

class Connect():
    CLIENT_ID = ""
    CLIENT_SECRET = ""
    SCOPE = ""
    FHIR_BASE_URL = ""
    payload = "grant_type=client_credentials&client_id={}&client_secret={}&scope={}".format(CLIENT_ID, CLIENT_SECRET, SCOPE)
    url = "https://login.microsoftonline.com/ca254449-06ec-4e1d-a3c9-f8b84e2afe3f/oauth2/v2.0/token"
    headers = { 'content-type': "application/x-www-form-urlencoded" }
    api_url = "https://json-fhir-tool.azurewebsites.net/api/json-fhir-tool"

    def get_access_token(self):  
        res = requests.post(Connect.url, Connect.payload, headers=Connect.headers)
        if res.status_code == 200:
            response_json = res.json()
            return response_json.get('access_token', None)

    def submit_blood_pressure(self, patient_id, systolic, diastolic):
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fz")
        token = self.get_access_token()
        body = {
            'token': token, 
            "fhir_url": "https://gosh-fhir-synth.azurehealthcareapis.com", 
            "date": date, 
            "systolic": int(systolic), 
            "diastolic": int(diastolic), 
            "patient_id": patient_id, 
            "type": "bloodpressure"
        }
        fhir = requests.post(Connect.api_url, json=body)
        if fhir.status_code == 200:
            if self.post_to_FHIR(fhir.json(), token) == 201:
                return body


    def submit_heart_rate(self, patient_id, heart_rate):
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fz")
        token = self.get_access_token()
        body = {
            "token": token, 
            "fhir_url": "https://gosh-fhir-synth.azurehealthcareapis.com", 
            "date": date, 
            "heartrate": int(heart_rate), 
            "patient_id": patient_id, 
            "type": "heartrate"
        }
        fhir = requests.post(Connect.api_url, json=body)
        if fhir.status_code == 200:
            if self.post_to_FHIR(fhir.json(), token) == 201:
                return body
        
    def post_to_FHIR(self, data, token):
        observation_url = "https://gosh-fhir-synth.azurehealthcareapis.com/Observation"
        status = requests.post(observation_url, json=data, headers={'content-type': "application/json", 'Authorization': 'Bearer ' + token})
        return status.status_code


    