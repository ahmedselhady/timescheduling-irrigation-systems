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

const Upload = () => {
  const router = useRouter();
  const {
    toggleShowResults,
    handleSaveData,
    pumpUnitValue,
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

    // const formData = new FormData();
    // if (uploadedFile === null) {
    //   alert("please enter a file");
    //   return;
    // }
    // formData.append("file", uploadedFile);
    // formData.append("pump_unit_estimated_gpm", String(pumpUnitValue));
    // try {
    //   const response = await fetch("http://127.0.0.1:5000/", {
    //     method: "POST",
    //     body: formData,
    //   });
    //   if (!response.ok) {
    //     console.log("here");
    //     throw new Error(`Error: ${response.statusText}`);
    //   }
    //   const result = await response.json();
    //   console.log(result);
    //   // Handle success however you prefer
    //   if (result) {
    //     toggleShowResults();
    //   }
    // } catch (error) {
    //   if (error instanceof Error) {
    //     console.error(error.message);
    //     // Handle error however you prefer
    //   }
    // }
  };

  return (
    <Card
      sx={{
        width: { xs: "100%", sm: "45rem" },
        padding: { xs: "2rem 0", sm: "2rem 3rem" },
      }}
    >
      <CardHeader title="Upload" sx={{ textAlign: "center" }}></CardHeader>
      <CardContent>
        <FormControl className="flex justify-center gap-8">
          <Input
            onChange={handleFileChange}
            type="file"
            className="custom-file-upload border-2 border-dashed bg-[#F8F8FF] h-[14.625rem] w-full"
            inputProps={{ style: { height: "100%" } }}
            sx={{ borderColor: "primary.main" }}
            disableUnderline
          />
          <InputLabel
            className="flex flex-col items-center justify-center w-full"
            shrink={false}
          >
            <DriveFolderUploadIcon
              sx={{ fontSize: "6rem", color: "#483EA8" }}
            />
            <Typography
              variant="h5"
              sx={{
                color: "#0F0F0F",
                fontWeight: "700",
                fontSize: "1rem",
              }}
              className="pt-7"
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
      <CardActions className="flex flex-col justify-center">
        <div className="flex justify-between py-7">
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
        <Button
          type="submit"
          onClick={handleFileUpload}
          sx={{ background: "#483EA8", width: "100%" }}
          variant="contained"
        >
          Calculate
        </Button>
      </CardActions>
    </Card>
  );
};

export default Upload;
