import * as React from "react";
import Box from "@mui/material/Box";
import Collapse from "@mui/material/Collapse";
import IconButton from "@mui/material/IconButton";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Typography from "@mui/material/Typography";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";

function createData(
  name: string,
  calories: number,
  fat: string,
  carbs: number,
  protein: number,
  price: number
) {
  return {
    name,
    calories,
    fat,
    carbs,
    protein,
    price,
    history: [
      { code: "G-HD132", value: 26.75 },
      { code: "G-HD140", value: 26.75 },
      { code: "G-HD198", value: 26.75 },
      { code: "K-HD59", value: 26.25 },
      { code: "E-HD189", value: 25.5 },
      { code: "G-HD199", value: 25.25 },
      { code: "E-HD184", value: 25.0 },
      { code: "G-HD111", value: 24.75 },
      { code: "J-HD86", value: 24.25 },
      { code: "K-HD225", value: 24.25 },
      { code: "H-HD255", value: 24.75 },
      { code: "H-HD153", value: 23.5 },
      { code: "J-HD70", value: 24.0 },
      { code: "E-HD191", value: 22.75 },
      { code: "G-HD123", value: 23.0 },
      { code: "G-HD193", value: 21.5 },
      { code: "K-HD38", value: 21.25 },
      { code: "E-HD186", value: 20.25 },
      { code: "G-HD194", value: 20.25 },
      { code: "I-HD117", value: 20.75 },
      { code: "H-HD164", value: 19.5 },
      { code: "G-HD141", value: 17.5 },
      { code: "I-HD131", value: 17.5 },
      { code: "K-HD20", value: 17.25 },
      { code: "K-HD231", value: 17.25 },
      { code: "H-HD163", value: 17.0 },
      { code: "K-HD40", value: 14.0 },
      { code: "K-HD16", value: 12.5 },
    ],
  };
}

export const rows = [
  createData("0", 610.0, "1/2", 28, 4.0, 3.99),
  createData("1", 312.0, "2/3", 31, 2.5, 3.99),
];

const GroupElement = (props: { row: ReturnType<typeof createData> }) => {
  const { row } = props;
  const [open, setOpen] = React.useState(false);

  return (
    <React.Fragment>
      <TableRow
        sx={{
          "& > *": { borderBottom: "unset" },
        }}
      >
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        <TableCell component="th" scope="row">
          {row.name}
        </TableCell>
        <TableCell align="right">{row.calories}</TableCell>
        <TableCell align="right">{row.fat}</TableCell>
        <TableCell align="right">{row.carbs}</TableCell>
      </TableRow>
      <TableRow className="overflow-hidden">
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              <Table size="medium" aria-label="purchases">
                <TableBody className="flex max-w-[57rem] overflow-x-scroll">
                  {row.history.map((historyRow) => (
                    <TableRow
                      key={historyRow.code}
                      hover
                      className="flex flex-col"
                    >
                      <TableCell className="whitespace-nowrap">
                        {historyRow.code}
                      </TableCell>
                      <TableCell className="">{historyRow.value}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
};

export default GroupElement;
