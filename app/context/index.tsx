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
  pumpUnitValue: string | number;
  pumpUnitValueInputHandler: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppWrapper({ children }: { children: React.ReactNode }) {
  // Layout

  const [drawerIsOpened, setDrawerIsOpen] = React.useState(false);
  const [groups, setGroups] = React.useState<ResponseData | null>(null);
  const [showResult, setShowGroups] = React.useState<boolean>(false);
  const [pumpUnitValue, setPumpUnitValue] = React.useState<number | string>("");

  const handleSaveData = (payload: ResponseData) => {
    setGroups(payload);
  };

  const handleDrawerToggle = () => {
    setDrawerIsOpen((prevState) => !prevState);
  };

  const toggleShowResults = () => {
    setShowGroups((preState) => !preState);
  };

  const pumpUnitValueInputHandler = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setPumpUnitValue(e.target.value);
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
        pumpUnitValue,
        pumpUnitValueInputHandler,
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
