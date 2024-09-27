"use client";

import React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import { useAppContext } from "@/context";
import CreateNewFolderIcon from "@mui/icons-material/CreateNewFolder";
import ListIcon from "@mui/icons-material/List";
import Image from "next/image";

import { drawerWidth } from "@/constants";
import Link from "next/link";
import logo from "@/assets/logo-Photoroom.png";

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

const DrawerEle = () => {
  const theme = useTheme();
  const { drawerIsOpened, handleDrawerToggle } = useAppContext();

  return (
    <Drawer
      disableEnforceFocus
      hideBackdrop
      ModalProps={{
        onBackdropClick: handleDrawerToggle,
        keepMounted: true,
        disableScrollLock: true,
      }}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
        },
      }}
      variant="temporary"
      anchor="left"
      open={drawerIsOpened}
    >
      <DrawerHeader className="flex items-center justify-between">
        <Image
          quality={100}
          src={logo}
          height={100}
          width={120}
          alt="logo"
          objectFit="cover"
        />
        <IconButton onClick={handleDrawerToggle}>
          {theme.direction === "ltr" ? (
            <ChevronLeftIcon />
          ) : (
            <ChevronRightIcon />
          )}
        </IconButton>
      </DrawerHeader>
      <Divider />
      <List>
        <Link href="/" onClick={handleDrawerToggle}>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <InboxIcon />
              </ListItemIcon>
              <ListItemText primary="New Schedule" />
            </ListItemButton>
          </ListItem>
        </Link>
      </List>
      <Divider />
      {/* <List>
        {["New Project", "List Project"].map((text, index) => (
          <ListItem key={text} disablePadding>
            <ListItemButton>
              <ListItemIcon>
                {index % 2 === 0 ? <CreateNewFolderIcon /> : <ListIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List> */}
    </Drawer>
  );
};

export default DrawerEle;
