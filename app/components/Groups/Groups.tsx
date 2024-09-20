import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import GroupElement from "./GroupElement";
import { rows } from "./GroupElement";

const Groups = () => {
  return (
    <TableContainer component={Paper} sx={{ maxWidth: "60rem" }}>
      <Table aria-label="collapsible table">
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell>Group ID</TableCell>
            <TableCell align="right">Group Total GPM</TableCell>
            <TableCell align="right">Pump Works</TableCell>
            <TableCell align="right">Number of Valves</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <GroupElement key={row.name} row={row} />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Groups;
