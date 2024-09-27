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
  FormGroup,
  FormControlLabel,
  TextField,
  Typography,
} from "@mui/material";
import Checkbox from "@mui/material/Checkbox";
import DriveFolderUploadIcon from "@mui/icons-material/DriveFolderUpload";
import { useAppContext } from "@/context";
import { useRouter } from "next/navigation";
import newData from "../../../new-example.json";

interface CheckboxState {
  acceptLower: boolean;
  acceptExact: boolean;
  acceptHigher: boolean;
}

const NewIrrigationScheduleForm = () => {
  const router = useRouter();
  const {
    toggleShowResults,
    handleSaveData,
    pumpUnitValue,
    isSmScreen,
    pumpUnitValueInputHandler,
  } = useAppContext();

  const [uploadedFile, setUploadedFile] = React.useState<File | null>(null);
  const [fileFormat, setFileFormat] = React.useState<string>("");

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

    setUploadedFile(file);
    if (file) {
      setFileFormat(file.name.split(".").pop() || "");
    }
  };

  const handleFileUpload = async (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    if (pumpUnitValue === "" || uploadedFile === null) {
      alert("please enter value or uplaod a file");
      return;
    }
    handleSaveData(newData);
    toggleShowResults();
    router.push("/results");
  };

  return (
    <Card
      sx={{
        padding: { xs: "0", sm: "2rem 3rem" },
      }}
    >
      <CardHeader
        title="New Irrigation Schedule"
        sx={{ textAlign: "center" }}
      ></CardHeader>
      <CardContent>
        <FormControl className="flex justify-center gap-8">
          <Input
            onChange={handleFileChange}
            type="file"
            className="custom-file-upload border-2 border-dashed bg-[#F8F8FF] h-[9rem] sm:h-[14.625rem] w-full"
            inputProps={{ style: { height: "100%" } }}
            sx={{ borderColor: "primary.main" }}
            disableUnderline
          />
          <InputLabel
            shrink={false}
            className="flex flex-col items-center justify-center w-full p-3 sm:p-0"
          >
            <DriveFolderUploadIcon
              sx={{ fontSize: { sm: "6rem", xs: "3rem" }, color: "#483EA8" }}
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
          <TextField
            required
            type="number"
            value={pumpUnitValue}
            onChange={(e: any) => pumpUnitValueInputHandler(e)}
            className="w-full"
            id="outlined-basic"
            label="Pump Unit Estimated GPM"
            variant="outlined"
          />
        </FormControl>
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
        <div className="w-full flex items-center justify-center my-4">
          <Button
            type="submit"
            onClick={handleFileUpload}
            sx={{ background: "#483EA8", width: "100%", padding: "0.75rem" }}
            variant="contained"
          >
            Calculate
          </Button>
        </div>
      </CardActions>
    </Card>
  );
};

export default NewIrrigationScheduleForm;
