import React from "react";

import NewIrrigationScheduleForm from "@/components/NewIrrigationScheduleForm/NewIrrigationScheduleForm";
import SnackbarAlert from "@/components/SnackBar/SnackBar";
import ModalAlert from "@/components/ModalAlert/ModalAlert";

export default function NewSchedule() {
  return (
    <>
      <NewIrrigationScheduleForm />
      <SnackbarAlert />
      <ModalAlert />
    </>
  );
}
