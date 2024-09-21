from flask import Flask, request
from flask_cors import CORS
from utils import file_parsing, format_handler
from pydantic import BaseModel, validator
import os

    
app = Flask(__name__)
CORS(app)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Schedule(BaseModel):
    pump_unit_estimated_gpm: confloat(gt = 0)

@app.route('/', methods = ['POST'])
def main():
     # Check if file is present in the request
    if 'data_file' not in request.files:
        return jsonify({'error' : 'No data file sent'}), 400
    
    data_file = request.files['data_file']
    # Check if a file is selected
    if data_file.filename == '':
        return jsonify({'error' : 'No selected file'}), 400

    file_extension = os.path.splitext(data_file.filename)[1]  # This will return extension like '.txt', '.jpg', etc.
    if file_extension not in ['.txt', '.xlsx']:
        return jsonify({'error': f'Invalid file extension {file_extension}, only .txt and .xlsx files are allowed'}), 400
    
    # pump_unit_estimated_gpm = float(pump_unit_estimated_gpm)
    try:
        pump_unit_estimated_gpm = Schedule(pump_unit_estimated_gpm = request.form['pump_unit_estimated_gpm'])
    except ValidationError as e: 
        return jsonify(e.errors()), 400
    
    file_name = f"data_file{file_extension}"
    data_file.save(os.path.join(UPLOAD_FOLDER, file_name))
    # schedule_result = schedule.create_schedule(file_name, pump_unit_estimated_gpm)
    
    with open("uploads/" + file_name, "r") as file:
        schedule_result = file_parsing.parse_file(file, pump_unit_estimated_gpm)
        schedule_result = format_handler.convert_to_json(schedule_result)
        # return result
    
    
    return schedule_result

if __name__ == '__main__':
    app.run(debug=True)