import * as React from "react";
import Box from "@mui/material/Box";
import Collapse from "@mui/material/Collapse";
import IconButton from "@mui/material/IconButton";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Typography from "@mui/material/Typography";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import { Group } from "@/type";
import { styled } from "@mui/material/styles";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

interface GroupElementProps {
  id: string;
  totalGpm: string | number;
  numberOfValves: number;
  groups: Group[];
}

const GroupElement = ({
  id,
  totalGpm,
  numberOfValves,
  groups,
}: GroupElementProps) => {
  const [openId, setOpenId] = React.useState<string | null>(null);
  const [insideOpenId, setInsideOpenId] = React.useState<string | null>(null);

  const handleClick = (groupId: string) => {
    if (openId === groupId) {
      setOpenId(null);
    } else {
      setOpenId(groupId);
    }
  };

  const handleInnerClick = (groupId: string, historyId: string) => {
    if (insideOpenId === historyId) {
      setInsideOpenId(null);
    } else {
      setInsideOpenId(historyId);
    }
  };

  return (
    <React.Fragment>
      <TableRow>
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => handleClick(id)}
          >
            {openId === id ? (
              <KeyboardArrowUpIcon />
            ) : (
              <KeyboardArrowDownIcon />
            )}
          </IconButton>
        </TableCell>
        <TableCell component="th" scope="row">
          {id}
        </TableCell>
        <TableCell align="right">{totalGpm}</TableCell>
        <TableCell align="right">{numberOfValves}</TableCell>
      </TableRow>
      {groups.map((rowItem) => (
        <StyledTableRow
          sx={{
            "& > *": { borderBottom: "unset" },
            bgcolor: insideOpenId === rowItem.id ? "#E3EEFA" : "inherit",
          }}
        >
          <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
            <Collapse in={openId === id} timeout="auto" unmountOnExit>
              {/*  */}

              <TableRow
                sx={{
                  "& > *": { borderBottom: "unset" },
                }}
              >
                <TableCell>
                  <IconButton
                    aria-label="expand row"
                    size="small"
                    onClick={() => handleInnerClick(id, rowItem.id)}
                  >
                    {insideOpenId === rowItem.id ? (
                      <KeyboardArrowUpIcon />
                    ) : (
                      <KeyboardArrowDownIcon />
                    )}
                  </IconButton>
                </TableCell>
                <TableCell component="th" scope="row">
                  Group ID: {rowItem.id}
                </TableCell>
                <TableCell align="right">
                  Group Total GPM: {rowItem.total_gpm}
                </TableCell>
                <TableCell align="right">
                  Pump Works: {rowItem.pump_works}
                </TableCell>
                <TableCell align="right">
                  Number of Valves: {rowItem.valves_number}
                </TableCell>
              </TableRow>
              <Collapse
                in={insideOpenId === rowItem.id}
                timeout="auto"
                unmountOnExit
              >
                <Box
                  sx={{
                    margin: 1,
                  }}
                >
                  <Table size="medium" aria-label="purchases">
                    <TableBody className="flex max-w-[57rem] overflow-x-scroll">
                      {rowItem.valves.map((valveItem) => (
                        <TableRow
                          key={valveItem.id}
                          hover
                          className="flex flex-col"
                        >
                          <TableCell className="whitespace-nowrap">
                            {valveItem.id}
                          </TableCell>
                          <TableCell className="">{valveItem.gpm}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </Box>
              </Collapse>

              {/*  */}
            </Collapse>
          </TableCell>
        </StyledTableRow>
      ))}
    </React.Fragment>
  );
};

export default GroupElement;
