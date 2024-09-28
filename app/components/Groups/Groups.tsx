"use client";

import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import { styled } from "@mui/material/styles";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { useAppContext } from "@/context";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { redirect } from "next/navigation";

const StyledTableRow = styled(TableRow)(() => ({
  "&:nth-of-type(odd)": {
    backgroundColor: "#ADD8E6",
  },
  "&:hover": {
    backgroundColor: "#8aadb8",
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

const Groups = () => {
  const { groups, pumpUnitValue } = useAppContext();

  React.useLayoutEffect(() => {
    if (groups === null) {
      redirect("/");
    }
  }, []);

  const countValvesForEachNetwork = () => {
    const networkValveCounts: any = {};

    groups?.batch_data.forEach((network: any) => {
      const networkName = network.network;

      let networkValveCount = 0;
      network.batchs.forEach((batch: any) => {
        for (const controllerKey in batch.controller_valves) {
          networkValveCount += batch.controller_valves[controllerKey].length;
        }
      });

      networkValveCounts[networkName] = networkValveCount;
    });

    return networkValveCounts;
  };

  const networkValveCounts = countValvesForEachNetwork();

  return (
    <div className="flex flex-col w-full sm:max-w-[95%] gap-8 my-4">
      <div className="flex items-center justify-center">
        <Card sx={{ width: "35rem" }}>
          <CardContent className="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-16 sm:gap-0 justify-between">
            <div>
              <Typography
                gutterBottom
                className="text-nowrap"
                sx={{ color: "text.secondary", fontSize: 14 }}
              >
                Estimated Pump GPM
              </Typography>
              <Typography variant="h5" component="div">
                {Number(pumpUnitValue).toFixed(1)}
              </Typography>
            </div>
            <div>
              <Typography
                gutterBottom
                sx={{ color: "text.secondary", fontSize: 14 }}
              >
                Pump Type
              </Typography>
              <Typography variant="h5" component="div">
                {groups?.pump_type === 3
                  ? "Triplet"
                  : groups?.pump_type === 2
                  ? "Double"
                  : groups?.pump_type === 1
                  ? "Single"
                  : "X"}
              </Typography>
            </div>
            <div>
              <Typography
                className="text-nowrap"
                gutterBottom
                sx={{ color: "text.secondary", fontSize: 14 }}
              >
                Total Number of batches
              </Typography>
              <Typography variant="h5" component="div">
                {groups?.total_num_batches}
              </Typography>
            </div>
          </CardContent>
        </Card>
      </div>
      <div className="flex flex-col gap-24">
        {groups?.batch_data.map((item) => (
          <div key={item.network} className="flex flex-col gap-3">
            <Card sx={{ width: "100%" }}>
              <CardContent className="flex flex-col sm:flex-row gap-4 md:gap-36">
                <div>
                  <Typography
                    variant="h5"
                    className="text-lg sm:text-2xl"
                    component="div"
                  >
                    <strong>{item.network}</strong>
                  </Typography>
                </div>
                <div>
                  <Typography
                    variant="h5"
                    component="div"
                    className="text-lg sm:text-2xl"
                  >
                    <strong>Total GPM:</strong>{" "}
                    {item.network_total_gpm.toFixed(3)}
                  </Typography>
                </div>
                <div>
                  <Typography
                    variant="h5"
                    component="div"
                    className="text-lg sm:text-2xl"
                  >
                    <strong> Number of valves: </strong>
                    {networkValveCounts[item.network] ?? "N/A"}
                  </Typography>
                </div>
              </CardContent>
            </Card>
            <TableContainer
              key={item.network}
              component={Paper}
              className="mx-auto  max-h-96"
            >
              <Table className="border-l bg-slate-50 flex">
                <Table>
                  <TableHead className="sm:text-nowrap">
                    <TableCell className="px-1 sm:px-3 bg-[#4ADEDE]">
                      Batch ID
                    </TableCell>
                    <TableCell className="bg-[#797EF6]">
                      # Valves / Batch
                    </TableCell>
                    <TableCell className="bg-[#1AA7EC]">
                      Total Batch GPM
                    </TableCell>
                  </TableHead>
                  <TableBody>
                    {item.batchs.map((batchsItem, index) => (
                      <React.Fragment key={`batch-${batchsItem.batch_id}`}>
                        <TableRow className="text-nowrap">
                          <TableCell className="bg-[#4ADEDE] px-1 sm:px-3">
                            Batch: <strong>{batchsItem.batch_id}</strong>
                          </TableCell>
                          <TableCell className="bg-[#797EF6]">
                            {Object.values(batchsItem.controller_valves).reduce(
                              (acc, curr) => acc + curr.length,
                              0
                            )}
                          </TableCell>
                          <TableCell className="bg-[#1AA7EC]">
                            {batchsItem.batch_total_gpm}
                          </TableCell>
                        </TableRow>
                        {/* Empty row below each batch row */}
                        <TableRow
                          className="text-nowrap"
                          key={`batch-${batchsItem.batch_id}`}
                        >
                          <TableCell className="bg-[#4ADEDE]"></TableCell>
                          <TableCell className="bg-[#797EF6]"></TableCell>
                          <TableCell className="bg-[#1AA7EC]">
                            {batchsItem.batch_total_gpm}
                          </TableCell>
                        </TableRow>
                      </React.Fragment>
                    ))}
                  </TableBody>
                </Table>
                <div className="overflow-x-scroll no-scrollbar border-l">
                  <TableHead>
                    <TableCell className="py-[3.25rem] sm:py-4">.</TableCell>
                  </TableHead>
                  <TableBody>
                    {item.batchs.map((batchItem) => (
                      <TableRow className="flex" key={batchItem.batch_id}>
                        {Object.values(batchItem.controller_valves)
                          .sort()
                          .map((controllerItem) =>
                            controllerItem.map(
                              (innerItem: [string, number]) => (
                                <TableRow
                                  key={innerItem[0]}
                                  hover
                                  className="min-w-[5.5rem] cursor-pointer"
                                >
                                  <StyledTableRow>
                                    <TableCell className="min-w-[5.5rem]">
                                      {innerItem[0]}
                                    </TableCell>
                                  </StyledTableRow>
                                  <TableRow>
                                    <TableCell className="min-w-[5.5rem]">
                                      {innerItem[1]}
                                    </TableCell>
                                  </TableRow>
                                </TableRow>
                              )
                            )
                          )}
                      </TableRow>
                    ))}
                  </TableBody>
                </div>
              </Table>
            </TableContainer>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Groups;
