"use client";

import React from "react";

import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  FormControl,
  Input,
  InputLabel,
  FormControlLabel,
  TextField,
  Typography,
  IconButton,
} from "@mui/material";
import WarningIcon from "@mui/icons-material/Warning";
import CircularProgress from "@mui/material/CircularProgress";
import Checkbox from "@mui/material/Checkbox";
import DriveFolderUploadIcon from "@mui/icons-material/DriveFolderUpload";
import { useAppContext } from "@/context";
import { useRouter } from "next/navigation";
import DescriptionIcon from "@mui/icons-material/Description";
import HighlightOffRoundedIcon from "@mui/icons-material/HighlightOffRounded";

interface CheckboxState {
  acceptLower: boolean;
  acceptExact: boolean;
  acceptHigher: boolean;
}

const NewIrrigationScheduleForm = () => {
  const router = useRouter();

  const {
    handleSaveData,
    pumpUnitValue,
    pumpUnitValueInputHandler,
    handleShowingSnackBar,
    handleShowingModal,
  } = useAppContext();

  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [isError, setIsError] = React.useState<boolean>(false);
  const [uploadedFile, setUploadedFile] = React.useState<File | null>(null);
  const [isWrongFormat, setIsWrongFormat] = React.useState<boolean>(false);

  const [checkboxes, setCheckboxes] = React.useState<CheckboxState>({
    acceptLower: false,
    acceptExact: true,
    acceptHigher: false,
  });

  const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCheckboxes({
      ...checkboxes,
      [event.target.name]: event.target.checked,
    });
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;
    if (file?.type !== "text/plain") {
      setIsWrongFormat(true);
      handleShowingSnackBar(true, {
        message: "Unsupported file type",
      });
      return;
    }
    setUploadedFile(file);
  };

  const validateForm = () => {
    let errorMessages = [];
    if (pumpUnitValue.toString().trim() === "" || Number(pumpUnitValue) < 0) {
      errorMessages.push("Cannot create a schedule for the given GPM");
    }
    if (
      !uploadedFile ||
      (uploadedFile.type && uploadedFile.type !== "text/plain")
    ) {
      setIsWrongFormat(true);
      errorMessages.push("Unsupported file type");
    }

    if (errorMessages.length > 0) {
      handleShowingSnackBar(true, {
        message: errorMessages.join(" & "),
      });
      errorMessages = [];
      return false;
    }
    return true;
  };

  const handleFileUpload = async (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    event.preventDefault();
    const formIsValid = validateForm();
    if (!formIsValid || !uploadedFile) {
      setIsError(true);
      return;
    }

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append("upload_file", uploadedFile);
      formData.append("pump_unit_estimated_gpm", pumpUnitValue.toString());
      formData.append("allow_exact", "true");
      formData.append("allow_oversampling", "False");
      formData.append("allow_undersampling", "False");

      const response = await fetch("http://62.84.182.54/schedule", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        setIsLoading(false);
        let data = localStorage.getItem("cachedData");
        if (!data) {
          handleShowingSnackBar(true, {
            message: "Cannot create a schedule for the given Data",
          });
          return;
        }
        let parsedData = JSON.parse(data);
        handleShowingModal(true, {
          title: "Cannot create a schedule for the given Data",
          message: "Do you want to use latest calculations",
          onConfirm: {
            label: "sure",
            action: async () => {
              handleSaveData(parsedData);
              router.push("/results");
            },
          },
          onDismiss: { label: "No", action: () => handleShowingModal(false) },
        });
        return;
      }

      const result = await response.json();
      setIsLoading(false);
      localStorage.setItem("cachedData", JSON.stringify(result));
      handleSaveData(result);
      router.push("/results");
    } catch (err) {
      setIsError(true);
      setIsLoading(false);
      console.error("There was an error uploading the file: ", err);
    }
  };

  return (
    <Card
      sx={{
        padding: { xs: "0", sm: "1rem 3rem" },
      }}
    >
      <CardHeader
        title="New Irrigation Schedule"
        sx={{ textAlign: "center" }}
      ></CardHeader>
      <CardContent>
        <FormControl className="flex justify-center gap-8">
          {!uploadedFile ? (
            <>
              <Input
                required
                onChange={handleFileChange}
                type="file"
                className="custom-file-upload border-2 border-dashed bg-[#F8F8FF] h-[9rem] sm:h-[14.625rem] w-full"
                inputProps={{ style: { height: "100%" } }}
                sx={{
                  borderColor: `${
                    !isWrongFormat ? "primary.main" : "error.main"
                  }`,
                }}
                disableUnderline
              />
              <InputLabel
                shrink={false}
                className="flex flex-col items-center justify-center w-full p-3 sm:p-0"
              >
                <DriveFolderUploadIcon
                  sx={{
                    fontSize: { sm: "6rem", xs: "3rem" },
                    color: "#483EA8",
                  }}
                />
                <Typography
                  variant="h5"
                  sx={{
                    color: "#0F0F0F",
                    fontWeight: "700",
                    fontSize: { sm: "1rem", xs: "0.75rem" },
                  }}
                  className="pt-3 sm:pt-7"
                >
                  Drag & drop files or
                  <span className="text-[#483EA8] underline"> Browse</span>
                </Typography>
                <Typography
                  variant="body2"
                  className="pt-3 text-[#676767] text-[0.75rem]"
                >
                  Limit 200MB per file
                </Typography>
              </InputLabel>
            </>
          ) : (
            <div className="flex items-center justify-between border-y-4 border-gray-500 border-opacity-20 w-full py-3">
              <div className="flex items-center gap-0 sm:gap-3">
                <DescriptionIcon color="primary" className="text-3xl" />
                <p className="text-sm">{uploadedFile.name}</p>
              </div>
              <div>
                <IconButton onClick={() => setUploadedFile(null)}>
                  <HighlightOffRoundedIcon className="" color="error" />
                </IconButton>
              </div>
            </div>
          )}
          <TextField
            required
            type="number"
            value={pumpUnitValue}
            InputProps={{ inputProps: { min: 0 } }}
            onChange={(e: any) => pumpUnitValueInputHandler(e)}
            className="w-full"
            id="outlined-basic"
            label="Pump Unit Estimated GPM"
            variant="outlined"
            error={
              (isError && pumpUnitValue.toString().trim() === "") ||
              Number(pumpUnitValue) < 0
            }
          />
        </FormControl>
        {isError && pumpUnitValue.toString().trim() === "" && (
          <InputLabel
            error
            className="absolute flex items-center gap-2 pt-2 text-sm"
          >
            <WarningIcon className="text-sm" />
            Incorrect entry.
          </InputLabel>
        )}
      </CardContent>
      <CardActions className="flex flex-col justify-center items-center">
        <div className="w-full flex flex-col sm:flex-row justify-between items-start pl-3 sm:pl-0 py-3 sm:py-7">
          <FormControlLabel
            control={
              <Checkbox
                name="acceptLower"
                checked={checkboxes.acceptLower}
                onChange={handleCheckboxChange}
              />
            }
            label="Accept 10% lower"
          />
          <FormControlLabel
            control={
              <Checkbox
                name="acceptExact"
                checked={checkboxes.acceptExact}
                onChange={handleCheckboxChange}
              />
            }
            label="Accept exact GPM"
          />
          <FormControlLabel
            control={
              <Checkbox
                name="acceptHigher"
                checked={checkboxes.acceptHigher}
                onChange={handleCheckboxChange}
              />
            }
            label="Accept 10% higher"
          />
        </div>
        <div className="w-full flex flex-col-reverse items-center justify-center my-4">
          <Button
            disabled={isLoading}
            type="submit"
            onClick={handleFileUpload}
            sx={{ width: "100%", padding: "0.75rem" }}
            variant="contained"
          >
            {!isLoading ? (
              "Calculate"
            ) : (
              <CircularProgress size="25px" sx={{ color: "white" }} />
            )}
          </Button>
        </div>
      </CardActions>
    </Card>
  );
};

export default NewIrrigationScheduleForm;
