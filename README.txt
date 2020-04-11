PatientCheckUp

This web application is used to submit forms to update information regarding the health of a patient stored in the FHIR records. It will currently allow you to submit the blood pressure and heart rate readings on specific patients, which are identified by their unique ID. The aim of this package is to help nurses efficiently log patient information using a fast and easy-to-use interface to save valuable time in the hospital.

The web app is built using the Python Flask framework as the backend along with static html and bootstrap for the frontend. The user input is saved as JSON with relevant information and posted to a JSON-to-FHIR tool, which returns the FHIR schema and is then ultimately sent to the FHIR server to add the observation for a specific patient. 

A FHIR parser is used to help identify a patient by their ID. https://pypi.org/project/FHIR-Parser/  (Apache License 2.0).

Installation and Setup:

pip install flask

python3 healthWebApp.py

Go to: http://localhost:8000

