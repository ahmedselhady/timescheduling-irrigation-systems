"use client";

import React, { useContext, createContext } from "react";

import { Batch, ResponseData } from "@/type";
import newData from "../../new-example.json";

interface AppContextType {
  drawerIsOpened: boolean;
  handleDrawerToggle: () => void;
  showResult: boolean;
  toggleShowResults: () => void;
  handleSaveData: (payload: ResponseData) => void;
  groups: ResponseData | null;
  arrangeControllersByBatch: (batch: Batch) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppWrapper({ children }: { children: React.ReactNode }) {
  // Layout

  const [drawerIsOpened, setDrawerIsOpen] = React.useState(false);
  const [groups, setGroups] = React.useState<ResponseData | null>(newData);
  const [showResult, setShowGroups] = React.useState<boolean>(false);

  const [controller, setController] = React.useState();

  // batch_id: number;
  // batch_total_gpm: number;
  // controller_valves: ValveData;

  const arrangeControllersByBatch = (batch: Batch) => {};

  const handleSaveData = (payload: ResponseData) => {
    setGroups(payload);
  };

  const handleDrawerToggle = () => {
    setDrawerIsOpen((prevState) => !prevState);
  };

  const toggleShowResults = () => {
    setShowGroups((preState) => !preState);
  };

  return (
    <AppContext.Provider
      value={{
        drawerIsOpened,
        handleDrawerToggle,
        showResult,
        toggleShowResults,
        handleSaveData,
        groups,
        arrangeControllersByBatch,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error("useAppContext must be used within an AppWrapper");
  }
  return context;
}