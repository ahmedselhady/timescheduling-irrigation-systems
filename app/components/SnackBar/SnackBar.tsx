"use client";

import * as React from "react";
import Button from "@mui/material/Button";
import Snackbar, { SnackbarCloseReason } from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import { useAppContext } from "@/context";
import { SnackbarProvider, VariantType, useSnackbar } from "notistack";

export default function SnackbarAlert() {
  const { enqueueSnackbar } = useSnackbar();

  const { handleShowingSnackBar, showSnackBar, snackBarData } = useAppContext();

  const handleClose = (
    event: React.SyntheticEvent | Event,
    reason?: SnackbarCloseReason
  ) => {
    if (reason === "clickaway") {
      return;
    }

    handleShowingSnackBar(false);
  };

  const action = (
    <React.Fragment>
      <Button
        color="primary"
        size="large"
        className="font-700"
        onClick={handleClose}
      >
        {snackBarData.action ? snackBarData.action : "ok"}
      </Button>
      <IconButton
        size="small"
        aria-label="close"
        color="inherit"
        onClick={handleClose}
      >
        <CloseIcon fontSize="small" />
      </IconButton>
    </React.Fragment>
  );

  return (
    <Snackbar
      open={showSnackBar}
      autoHideDuration={6000}
      onClose={handleClose}
      message={
        snackBarData.message ? snackBarData.message : "Something Went Wrong"
      }
      action={action}
    />
  );
}
