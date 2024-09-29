"use client";

import React, { useContext, createContext } from "react";

import { ResponseData } from "@/type";
import { useTheme, useMediaQuery } from "@material-ui/core";
import { usePathname } from "next/navigation";

interface SnackbarData {
  message: string;
  action?: string;
  actionHandler?: () => void;
}

interface Modal {
  title: string;
  message: string;
  onConfirm: {
    label: string;
    action?: () => void;
  };
  onDismiss: {
    label: string;
    action?: () => void;
  };
}

interface AppContextType {
  drawerIsOpened: boolean;
  handleDrawerToggle: () => void;
  handleSaveData: (payload: ResponseData) => void;
  groups: ResponseData | null;
  pumpUnitValue: string | number;
  pumpUnitValueInputHandler: (e: React.ChangeEvent<HTMLInputElement>) => void;
  isSmScreen: boolean;
  showSnackBar: boolean;
  handleShowingSnackBar: (show: boolean, data?: SnackbarData) => void;
  snackBarData: SnackbarData;
  showModal: boolean;
  handleShowingModal: (show: boolean, data?: Modal) => void;
  modalData: Modal;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppWrapper({ children }: { children: React.ReactNode }) {
  const pathName = usePathname();
  // Layout
  const theme = useTheme();
  const isMdScreen = useMediaQuery(theme.breakpoints.down("md"));
  const isSmScreen = useMediaQuery(theme.breakpoints.down("xs"));

  const [drawerIsOpened, setDrawerIsOpen] = React.useState(!isMdScreen);

  React.useEffect(() => {
    if (pathName === "/results" && drawerIsOpened) {
      setDrawerIsOpen(false);
    }
  }, [pathName]);

  const [groups, setGroups] = React.useState<ResponseData | null>(null);
  const [pumpUnitValue, setPumpUnitValue] = React.useState<number | string>("");

  const [showSnackBar, setShowSnackBar] = React.useState(false);
  const [snackBarData, setSnackBarData] = React.useState<SnackbarData>({
    message: "",
    action: "",
    actionHandler: () => {},
  });

  const [showModal, setShowModal] = React.useState(false);
  const [modalData, setModalData] = React.useState<Modal>({
    title: "",
    message: "",
    onConfirm: { action: () => {}, label: "" },
    onDismiss: { action: () => {}, label: "" },
  });

  React.useEffect(() => {
    if (isMdScreen) {
      setDrawerIsOpen(false);
    } else if (!isMdScreen) {
      setDrawerIsOpen(true);
    }
  }, [isMdScreen]);

  const handleShowingSnackBar = (show: boolean, data?: SnackbarData) => {
    setShowSnackBar(show);
    if (data) {
      setSnackBarData(data);
    }
  };
  const handleShowingModal = (show: boolean, data?: Modal) => {
    setShowModal(show);
    if (data) {
      setModalData(data);
    }
  };

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
        handleShowingSnackBar,
        showSnackBar,
        snackBarData,
        showModal,
        handleShowingModal,
        modalData,
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
