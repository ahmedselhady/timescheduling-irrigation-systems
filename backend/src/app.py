from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel, confloat
from utils import file_parsing, format_handler
import os

app = FastAPI()

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Schedule(BaseModel):
    pump_unit_estimated_gpm: confloat(gt = 0)
    
@app.post("/")
async def main(
    data_file: UploadFile = File(...), 
    pump_unit_estimated_gpm: float = Form(...)
):
    # Check file extension
    file_extension = os.path.splitext(data_file.filename)[1]
    if file_extension not in ['.txt', '.xlsx']:
        raise HTTPException(status_code=400, detail=f"Invalid file extension {file_extension}")

    # Save the file
    file_name = f"data_file{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    with open(file_path, "wb") as f:
        f.write(await data_file.read())
    
    with open("uploads/" + file_name, "r") as file:
        schedule_result = file_parsing.parse_file(file, pump_unit_estimated_gpm)
        schedule_result = format_handler.convert_to_json(schedule_result)
        # return result
    return schedule_result