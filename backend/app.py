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
    file_extension = os.path.splitext(data_file.filename)[1]  # This will return extension like '.txt', '.jpg', etc.
    pump_unit_estimated_gpm = request.form['pump_unit_estimated_gpm']
    pump_unit_estimated_gpm = float(pump_unit_estimated_gpm)
    # Check if a file is selected
    if data_file.filename == '':
        return 'No selected file', 400
    
    file_name = f"data_file{file_extension}"
    data_file.save(os.path.join(UPLOAD_FOLDER, file_name))
    schedule_result = schedule.create_schedule(file_name, pump_unit_estimated_gpm)
    return schedule_result

if __name__ == '__main__':
    app.run(debug=True)