from flask import Flask, request
from flask_cors import CORS
from models import schedule

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/', methods = ['POST'])
def main():
    data = request.get_json()
    pump_unit_estimated_gpm = data['pump_unit_estimated_gpm']
    pump_unit_estimated_gpm = float(pump_unit_estimated_gpm)
    print(pump_unit_estimated_gpm)
    schedule_result = schedule.create_schedule(pump_unit_estimated_gpm)
    return schedule_result

if __name__ == '__main__':
    app.run(debug=True)