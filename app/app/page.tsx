import React from "react";

import NewIrrigationScheduleForm from "@/components/NewIrrigationScheduleForm/NewIrrigationScheduleForm";
import SnackbarAlert from "@/components/SnackBar/SnackBar";

export default function NewSchedule() {
  return (
    <>
      <NewIrrigationScheduleForm />
      <SnackbarAlert />
    </>
  );
}
