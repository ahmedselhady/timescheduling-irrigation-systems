"use client";

import React, { useContext, createContext } from "react";

import { ResponseData } from "@/type";
import { useTheme, useMediaQuery } from "@material-ui/core";

interface AppContextType {
  drawerIsOpened: boolean;
  handleDrawerToggle: () => void;
  handleSaveData: (payload: ResponseData) => void;
  groups: ResponseData | null;
  pumpUnitValue: string | number;
  pumpUnitValueInputHandler: (e: React.ChangeEvent<HTMLInputElement>) => void;
  isSmScreen: boolean;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppWrapper({ children }: { children: React.ReactNode }) {
  // Layout
  const theme = useTheme();
  const isMdScreen = useMediaQuery(theme.breakpoints.down("md"));
  const isSmScreen = useMediaQuery(theme.breakpoints.down("xs"));

  const [drawerIsOpened, setDrawerIsOpen] = React.useState(!isMdScreen);
  const [groups, setGroups] = React.useState<ResponseData | null>(null);
  const [pumpUnitValue, setPumpUnitValue] = React.useState<number | string>("");

  React.useEffect(() => {
    if (isMdScreen) {
      setDrawerIsOpen(false);
    } else if (!isMdScreen) {
      setDrawerIsOpen(true);
    }
  }, [isMdScreen]);

  const handleSaveData = (payload: ResponseData) => {
    setGroups(payload);
  };

  const handleDrawerToggle = () => {
    setDrawerIsOpen((prevState) => !prevState);
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
        handleSaveData,
        groups,
        pumpUnitValue,
        pumpUnitValueInputHandler,
        isSmScreen,
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
