from flask import Flask, request
from flask_cors import CORS
from models import schedule
import os

app = Flask(__name__)
CORS(app)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods = ['POST'])
def main():
     # Check if file is present in the request
    if 'data_file' not in request.files:
        return 'No data file sent', 400
    
    # Check if number is present in the form data
    if 'pump_unit_estimated_gpm' not in request.form:
        return 'No pump_unit_estimated_gpm provided', 400
    
    data_file = request.files['data_file']
    pump_unit_estimated_gpm = request.form['pump_unit_estimated_gpm']
    
    # Check if a file is selected
    if data_file.filename == '':
        return 'No selected file', 400
    
    
    # data = request.get_json()
    # pump_unit_estimated_gpm = data['pump_unit_estimated_gpm']
    # pump_unit_estimated_gpm = float(pump_unit_estimated_gpm)
    print(float(pump_unit_estimated_gpm))
    schedule_result = schedule.create_schedule(data_file, pump_unit_estimated_gpm)
    return schedule_result

if __name__ == '__main__':
    app.run(debug=True)