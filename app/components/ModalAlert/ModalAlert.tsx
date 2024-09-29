"use client";

import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import { useAppContext } from "@/context";
import WarningIcon from "@mui/icons-material/Warning";

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export default function ModalAlert() {
  const { showModal, handleShowingModal, modalData } = useAppContext();
  const {
    title = "",
    message = "",
    onConfirm = { action: () => {}, label: "" },
    onDismiss = { action: () => {}, label: "" },
  } = modalData || {};

  return (
    <Modal
      open={showModal}
      onClose={() => handleShowingModal(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        {modalData && (
          <div className="flex flex-col items-center justify-center">
            <WarningIcon className="text-6xl mb-4" color="error" />
            <Typography
              id="modal-modal-title"
              variant="h6"
              className="font-semibold text-xl text-center"
              component="h2"
            >
              {title}
            </Typography>
            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
              {message}
            </Typography>
            <div className="flex gap-4 pt-5">
              <Button
                onClick={onConfirm.action}
                color="primary"
                variant="contained"
              >
                {onConfirm.label}
              </Button>
              <Button
                onClick={onDismiss.action}
                color="error"
                variant="contained"
              >
                {onDismiss.label}
              </Button>
            </div>
          </div>
        )}
      </Box>
    </Modal>
  );
}
