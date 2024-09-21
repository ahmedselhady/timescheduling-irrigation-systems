"use client";

import React, { useContext, createContext } from "react";
import { GroupCategory } from "@/type";

interface AppContextType {
  drawerIsOpened: boolean;
  handleDrawerToggle: () => void;
  showResult: boolean;
  toggleShowResults: () => void;
  handleSaveData: (payload: GroupCategory[]) => void;
  groups: GroupCategory[] | null;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppWrapper({ children }: { children: React.ReactNode }) {
  // Layout

  const [drawerIsOpened, setDrawerIsOpen] = React.useState(false);
  const [groups, setGroups] = React.useState<GroupCategory[] | null>(null);
  const [showResult, setShowGroups] = React.useState<boolean>(false);

  const handleSaveData = (payload: GroupCategory[]) => {
    console.log(payload);
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
