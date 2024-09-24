"use client";

import React from "react";

import { styled } from "@mui/material/styles";
import { useAppContext } from "@/context";

import Upload from "@/components/Upload/Upload";
import Groups from "@/components/Groups/Groups";
import Table from "@/components/Groups/Table";
import { Batch } from "@/type";

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

const Main = styled("main", { shouldForwardProp: (prop) => prop !== "open" })<{
  open?: boolean;
}>(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  transition: theme.transitions.create("margin", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  // marginLeft: `-${drawerWidth}px`,
  variants: [
    {
      props: ({ open }) => open,
      style: {
        transition: theme.transitions.create("margin", {
          easing: theme.transitions.easing.easeOut,
          duration: theme.transitions.duration.enteringScreen,
        }),
        marginLeft: 0,
      },
    },
  ],
}));

export default function Home() {
  const { drawerIsOpened, showResult } = useAppContext();

  return (
    <Main
      open={drawerIsOpened}
      className="flex items-center justify-center w-full"
      sx={{ marginTop: "6rem" }}
    >
      <DrawerHeader />
      {!showResult ? <Upload /> : <Groups />}
    </Main>
  );
}
