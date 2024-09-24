import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import { styled } from "@mui/material/styles";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import GroupElement from "./GroupElement";
import { useAppContext } from "@/context";

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

const Groups = () => {
  const { groups, arrangeControllersByBatch } = useAppContext();

  return (
    <div className="flex flex-col w-full gap-32">
      {groups?.batch_data.map((item) => (
        <TableContainer
          key={item.network}
          component={Paper}
          className="flex max-w-[80%] mx-auto  max-h-96"
        >
          <Table className="border-l bg-slate-50 flex">
            <Table>
              <TableHead className="text-nowrap">
                <TableCell>Batch ID</TableCell>
                <TableCell># Valves / Batch</TableCell>
                <TableCell>Total Batch GPM</TableCell>
              </TableHead>
              <TableBody>
                {item.batchs.map((batchsItem, index) => (
                  <React.Fragment key={`fragment-${batchsItem.batch_id}`}>
                    <TableRow
                      className="text-nowrap"
                      key={`batch-${batchsItem.batch_id}`}
                    >
                      <TableCell>
                        Batch: <strong>{batchsItem.batch_id}</strong>
                      </TableCell>
                      <TableCell>
                        {Object.values(batchsItem.controller_valves).reduce(
                          (acc, curr) => acc + curr.length,
                          0
                        )}
                      </TableCell>
                      <TableCell>{batchsItem.batch_total_gpm}</TableCell>
                    </TableRow>
                    {/* Empty row below each batch row */}
                    <TableRow key={`empty-${index}`}>
                      <TableCell colSpan={3}>.</TableCell>
                    </TableRow>
                  </React.Fragment>
                ))}
              </TableBody>
            </Table>
            <div className="overflow-x-scroll h-max">
              <TableHead>
                <TableCell>.</TableCell>
              </TableHead>
              <TableBody>
                {item.batchs.map((batchItem) => (
                  <TableRow className="flex">
                    {Object.values(batchItem.controller_valves)
                      .sort()
                      .map((controllerItem) =>
                        controllerItem.map((innerItem) => (
                          <TableRow hover className=" min-w-fit">
                            <StyledTableRow>
                              <TableCell>{innerItem[0]}</TableCell>
                            </StyledTableRow>
                            <TableRow>
                              <TableCell>{innerItem[1]}</TableCell>
                            </TableRow>
                          </TableRow>
                        ))
                      )}
                  </TableRow>
                ))}
              </TableBody>
            </div>
          </Table>
        </TableContainer>
      ))}
    </div>
  );
};

export default Groups;
