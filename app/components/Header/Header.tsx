"use client";

import React from "react";
import { styled } from "@mui/material/styles";
import MuiAppBar, { AppBarProps as MuiAppBarProps } from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import { useAppContext } from "@/context";

import logo from "@/assets/logo.jpeg";

import { drawerWidth } from "@/constants";
import Image from "next/image";

interface AppBarProps extends MuiAppBarProps {
  open?: boolean;
}

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})<AppBarProps>(({ theme }) => ({
  transition: theme.transitions.create(["margin", "width"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  variants: [
    {
      props: ({ open }) => open,
      style: {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: `${drawerWidth}px`,
        transition: theme.transitions.create(["margin", "width"], {
          easing: theme.transitions.easing.easeOut,
          duration: theme.transitions.duration.enteringScreen,
        }),
      },
    },
  ],
}));

const Header = () => {
  const { drawerIsOpened, handleDrawerToggle } = useAppContext();
  return (
    <AppBar position="fixed" open={drawerIsOpened}>
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          onClick={handleDrawerToggle}
          edge="start"
          sx={[
            {
              mr: 2,
            },
            drawerIsOpened && { display: "none" },
          ]}
        >
          <MenuIcon />
        </IconButton>
        <div className={`relative py-2 ${drawerIsOpened ? "hidden" : "block"}`}>
          <Image quality={100} width={100} height={100} src={logo} alt="logo" />
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
