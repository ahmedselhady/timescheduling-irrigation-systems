from fastapi import APIRouter, Depends, UploadFile, HTTPException, Form, File
from pydantic import BaseModel, conint, validator
from models.algorithm import irregation_scheduling_algorithm
import os


router = APIRouter()


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Schedule(BaseModel):
    upload_file: UploadFile  # Keep it here for validation
    pump_unit_estimated_gpm: conint(gt=0)
    allow_exact: bool
    allow_oversampling: bool
    allow_undersampling: bool

    @validator("upload_file")
    def validate_file(cls, v):
        file_extension = os.path.splitext(v.filename)[1]
        if file_extension not in [".txt", ".xlsx"]:
            raise ValueError(
                f"Invalid file extension {file_extension}. Must be .txt or .xlsx"
            )
        return v


@router.post("/schedule")
async def schedule(
    upload_file: UploadFile = File(...),
    pump_unit_estimated_gpm: float = Form(...),
    allow_exact: bool = Form(),
    allow_oversampling: bool = Form(),
    allow_undersampling: bool = Form(),
):
    try:
        # Validate the upload file directly
        Schedule(
            upload_file=upload_file,
            pump_unit_estimated_gpm=pump_unit_estimated_gpm,
            allow_exact=allow_exact,
            allow_oversampling=allow_oversampling,
            allow_undersampling=allow_undersampling,
        )


        # Save the file
        file_extension = os.path.splitext(upload_file.filename)[1]
        file_name = f"upload_file{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        with open(file_path, "wb") as f:
            f.write(await upload_file.read())

        response = irregation_scheduling_algorithm(
            uploaded_file=file_path,
            pump_unit_estimated_gpm=pump_unit_estimated_gpm,
            allow_exact=allow_exact,
            allow_oversampling=allow_oversampling,
            allow_undersampling=allow_undersampling,
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
