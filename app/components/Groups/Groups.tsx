import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import GroupElement from "./GroupElement";
import { useAppContext } from "@/context";

const Groups = () => {
  const { groups } = useAppContext();
  return (
    // maxWidth: "60rem"
    <TableContainer component={Paper} sx={{ maxWidth: "60rem" }}>
      <Table aria-label="collapsible table">
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell>Group ID</TableCell>
            <TableCell align="right">Group Total GPM</TableCell>
            <TableCell align="right">number of valves</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {groups?.map((row) => (
            <GroupElement
              key={row.group_id}
              id={row.group_id}
              totalGpm={row.total_gpm}
              numberOfValves={row.total_num_valves}
              groups={row.groups}
            />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Groups;
