"use client";

import React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { useAppContext } from "@/context";

const Groupsv2 = () => {
  const { groups } = useAppContext();

  return (
    <div className="flex mx-auto flex-col w-full gap-32 mt-28 max-w-[80%]">
      {groups?.batch_data.map((network) => (
        <TableContainer
          key={network.network}
          component={Paper}
          sx={{ maxWidth: "100%" }}
        >
          <Table aria-label="table">
            <TableHead>
              <TableRow>
                <TableCell>Network</TableCell>
                <TableCell>Batch ID</TableCell>
                <TableCell>Controller</TableCell>
                <TableCell>Valves</TableCell>
                <TableCell>Total Batch GPM</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {network.batchs.map((batch) => {
                return Object.entries(batch.controller_valves).map(
                  ([controller, valves], index) => (
                    <TableRow key={`${batch.batch_id}-${controller}-${index}`}>
                      <TableCell component="th" scope="row">
                        {index === 0 && network.network}
                      </TableCell>
                      <TableCell>{index === 0 && batch.batch_id}</TableCell>
                      <TableCell>{controller}</TableCell>
                      <TableCell>
                        {valves.map((valve) => (
                          <div key={`${controller}-${valve[0]}`}>
                            {valve[0]} - {valve[1]} GPM
                          </div>
                        ))}
                      </TableCell>
                      <TableCell>
                        {index === 0 && batch.batch_total_gpm}
                      </TableCell>
                    </TableRow>
                  )
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      ))}
    </div>
  );
};

export default Groupsv2;
