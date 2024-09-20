"use client";

import React, { useContext, createContext } from "react";

interface AppContextType {
  drawerIsOpened: boolean;
  handleDrawerToggle: () => void;
  showResult: boolean;
  toggleShowResults: () => void;
}
interface Valve {
  gpm: number;
  id: string;
}

interface Group {
  id: string;
  pump_works: string;
  total_gpm: string;
  valves: Valve[];
  valves_number: string;
}

interface GroupContainer {
  group_id: string;
  groups: Group[];
  total_gpm: string | number;
  total_num_valves: number;
}

type DataArray = GroupContainer[];

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppWrapper({ children }: { children: React.ReactNode }) {
  // Layout

  const DUMMYDATA = [
    {
      group_id: "B",
      groups: [
        {
          id: " 0",
          pump_works: " 2/3",
          total_gpm: " 607.25",
          valves: [
            {
              gpm: 30,
              id: "E-B137",
            },
            {
              gpm: 28.5,
              id: "C-B78",
            },
            {
              gpm: 28.5,
              id: "C-B85",
            },
            {
              gpm: 29,
              id: "F-B152",
            },
            {
              gpm: 26.25,
              id: "A-B37",
            },
            {
              gpm: 26.25,
              id: "C-B102",
            },
            {
              gpm: 27,
              id: "C-B105",
            },
            {
              gpm: 25.75,
              id: "D-B119",
            },
            {
              gpm: 24.75,
              id: "B-B42",
            },
            {
              gpm: 24.75,
              id: "B-B74",
            },
            {
              gpm: 23.25,
              id: "B-B51",
            },
            {
              gpm: 24,
              id: "B-B65",
            },
            {
              gpm: 24,
              id: "D-B120",
            },
            {
              gpm: 24,
              id: "F-B149",
            },
            {
              gpm: 24,
              id: "F-B150",
            },
            {
              gpm: 22,
              id: "A-B05",
            },
            {
              gpm: 21.75,
              id: "D-B109",
            },
            {
              gpm: 21,
              id: "A-B09",
            },
            {
              gpm: 20.25,
              id: "C-B95",
            },
            {
              gpm: 20.25,
              id: "D-B123",
            },
            {
              gpm: 18.75,
              id: "B-B44",
            },
            {
              gpm: 18,
              id: "B-B72",
            },
            {
              gpm: 16.5,
              id: "D-B113",
            },
            {
              gpm: 17,
              id: "E-B142",
            },
            {
              gpm: 15.5,
              id: "C-B77",
            },
            {
              gpm: 15.75,
              id: "D-B108",
            },
            {
              gpm: 10.5,
              id: "C-B75",
            },
          ],
          valves_number: " 27",
        },
        {
          id: " 1",
          pump_works: " 3/3",
          total_gpm: " 959.0",
          valves: [
            {
              gpm: 42,
              id: "D-B117",
            },
            {
              gpm: 42,
              id: "E-B140",
            },
            {
              gpm: 40.5,
              id: "A-B31",
            },
            {
              gpm: 40.5,
              id: "F-B148",
            },
            {
              gpm: 39,
              id: "B-B57",
            },
            {
              gpm: 39,
              id: "C-B93",
            },
            {
              gpm: 38.25,
              id: "D-B128",
            },
            {
              gpm: 37.5,
              id: "C-B100",
            },
            {
              gpm: 36.5,
              id: "A-B03",
            },
            {
              gpm: 37,
              id: "E-B136",
            },
            {
              gpm: 36,
              id: "A-B21",
            },
            {
              gpm: 36,
              id: "A-B29",
            },
            {
              gpm: 36,
              id: "B-B53",
            },
            {
              gpm: 36,
              id: "C-B79",
            },
            {
              gpm: 34.5,
              id: "A-B22",
            },
            {
              gpm: 34.5,
              id: "B-B43",
            },
            {
              gpm: 35,
              id: "E-B138",
            },
            {
              gpm: 34,
              id: "E-B155",
            },
            {
              gpm: 33,
              id: "A-B16",
            },
            {
              gpm: 32.25,
              id: "A-B32",
            },
            {
              gpm: 32.25,
              id: "B-B41",
            },
            {
              gpm: 32.25,
              id: "B-B59",
            },
            {
              gpm: 32,
              id: "F-B153",
            },
            {
              gpm: 32,
              id: "F-B147",
            },
            {
              gpm: 30.75,
              id: "B-B62",
            },
            {
              gpm: 31,
              id: "E-B141",
            },
            {
              gpm: 29.25,
              id: "B-B52",
            },
          ],
          valves_number: " 27",
        },
        {
          id: " 2",
          pump_works: " 3/3",
          total_gpm: " 1220.75",
          valves: [
            {
              gpm: 48.75,
              id: "B-B71",
            },
            {
              gpm: 48.75,
              id: "C-B96",
            },
            {
              gpm: 48.75,
              id: "C-B84",
            },
            {
              gpm: 47.25,
              id: "A-B18",
            },
            {
              gpm: 48,
              id: "B-B55",
            },
            {
              gpm: 48,
              id: "B-B58",
            },
            {
              gpm: 48,
              id: "B-B67",
            },
            {
              gpm: 47.25,
              id: "C-B92",
            },
            {
              gpm: 48,
              id: "D-B112",
            },
            {
              gpm: 47.25,
              id: "E-B157",
            },
            {
              gpm: 46.5,
              id: "C-B94",
            },
            {
              gpm: 46.5,
              id: "C-B82",
            },
            {
              gpm: 44.25,
              id: "A-B36",
            },
            {
              gpm: 45,
              id: "B-B64",
            },
            {
              gpm: 44.25,
              id: "C-B103",
            },
            {
              gpm: 43.5,
              id: "C-B99",
            },
            {
              gpm: 43.5,
              id: "D-B110",
            },
            {
              gpm: 43.5,
              id: "D-B129",
            },
            {
              gpm: 44,
              id: "E-B143",
            },
            {
              gpm: 43,
              id: "A-B11",
            },
            {
              gpm: 42.75,
              id: "B-B69",
            },
            {
              gpm: 42.75,
              id: "C-B101",
            },
            {
              gpm: 43,
              id: "E-B144",
            },
            {
              gpm: 43,
              id: "E-B139",
            },
            {
              gpm: 42,
              id: "A-B39",
            },
            {
              gpm: 42,
              id: "B-B54",
            },
            {
              gpm: 41.25,
              id: "C-B90",
            },
          ],
          valves_number: " 27",
        },
        {
          id: " 3",
          pump_works: " 3/3",
          total_gpm: " 1237.25",
          valves: [
            {
              gpm: 60,
              id: "E-B145",
            },
            {
              gpm: 57.75,
              id: "A-B25",
            },
            {
              gpm: 57.75,
              id: "B-B56",
            },
            {
              gpm: 58,
              id: "D-B116",
            },
            {
              gpm: 57.75,
              id: "D-B121",
            },
            {
              gpm: 56.25,
              id: "B-B68",
            },
            {
              gpm: 57,
              id: "B-B70",
            },
            {
              gpm: 56.25,
              id: "C-B80",
            },
            {
              gpm: 56.5,
              id: "F-B146",
            },
            {
              gpm: 55.5,
              id: "C-B86",
            },
            {
              gpm: 54.5,
              id: "D-B130",
            },
            {
              gpm: 53.25,
              id: "B-B60",
            },
            {
              gpm: 53.25,
              id: "C-B98",
            },
            {
              gpm: 52.5,
              id: "B-B47",
            },
            {
              gpm: 51.75,
              id: "A-B28",
            },
            {
              gpm: 51,
              id: "C-B91",
            },
            {
              gpm: 50.25,
              id: "C-B88",
            },
            {
              gpm: 50.25,
              id: "D-B132",
            },
            {
              gpm: 50.25,
              id: "E-B158",
            },
            {
              gpm: 49.5,
              id: "A-B17",
            },
            {
              gpm: 49.5,
              id: "B-B45",
            },
            {
              gpm: 50,
              id: "F-B154",
            },
            {
              gpm: 48.5,
              id: "A-B04",
            },
          ],
          valves_number: " 23",
        },
        {
          id: " 4",
          pump_works: " 3/3",
          total_gpm: " 1239.5",
          valves: [
            {
              gpm: 64.5,
              id: "C-B97",
            },
            {
              gpm: 63.75,
              id: "A-B14",
            },
            {
              gpm: 63.75,
              id: "A-B24",
            },
            {
              gpm: 63.75,
              id: "C-B83",
            },
            {
              gpm: 63.75,
              id: "D-B126",
            },
            {
              gpm: 63.75,
              id: "D-B127",
            },
            {
              gpm: 62.5,
              id: "A-B10",
            },
            {
              gpm: 62.25,
              id: "A-B23",
            },
            {
              gpm: 62.25,
              id: "A-B40",
            },
            {
              gpm: 62.25,
              id: "B-B61",
            },
            {
              gpm: 63,
              id: "C-B104",
            },
            {
              gpm: 62.25,
              id: "C-B106",
            },
            {
              gpm: 61.5,
              id: "B-B63",
            },
            {
              gpm: 61.75,
              id: "B-B73",
            },
            {
              gpm: 60.75,
              id: "A-B26",
            },
            {
              gpm: 60,
              id: "A-B19",
            },
            {
              gpm: 59.25,
              id: "A-B34",
            },
            {
              gpm: 59.25,
              id: "D-B111",
            },
            {
              gpm: 59.25,
              id: "D-B118",
            },
            {
              gpm: 60,
              id: "E-B156",
            },
          ],
          valves_number: " 20",
        },
        {
          id: " 5",
          pump_works: " 3/3",
          total_gpm: " 1280.5",
          valves: [
            {
              gpm: 72.75,
              id: "D-B131",
            },
            {
              gpm: 71.25,
              id: "B-B46",
            },
            {
              gpm: 72,
              id: "D-B115",
            },
            {
              gpm: 70.25,
              id: "D-B133",
            },
            {
              gpm: 70.5,
              id: "D-B125",
            },
            {
              gpm: 69.25,
              id: "A-B12",
            },
            {
              gpm: 68.25,
              id: "D-B107",
            },
            {
              gpm: 67,
              id: "A-B06",
            },
            {
              gpm: 66.75,
              id: "A-B35",
            },
            {
              gpm: 66.75,
              id: "D-B122",
            },
            {
              gpm: 66,
              id: "B-B50",
            },
            {
              gpm: 66,
              id: "B-B66",
            },
            {
              gpm: 65.25,
              id: "C-B76",
            },
            {
              gpm: 65.25,
              id: "D-B134",
            },
            {
              gpm: 65,
              id: "A-B02",
            },
            {
              gpm: 64.75,
              id: "A-B08",
            },
            {
              gpm: 64.5,
              id: "A-B27",
            },
            {
              gpm: 64.5,
              id: "A-B38",
            },
            {
              gpm: 64.5,
              id: "B-B49",
            },
          ],
          valves_number: " 19",
        },
      ],
      total_gpm: 6544.25,
      total_num_valves: 143,
    },
    {
      group_id: "HD",
      groups: [
        {
          id: " 0",
          pump_works: " 2/2",
          total_gpm: " 821.0",
          valves: [
            {
              gpm: 53,
              id: "E-HD71",
            },
            {
              gpm: 51.5,
              id: "C-HD112",
            },
            {
              gpm: 50.5,
              id: "C-HD103",
            },
            {
              gpm: 47.5,
              id: "E-HD68",
            },
            {
              gpm: 45.75,
              id: "E-HD63",
            },
            {
              gpm: 45,
              id: "E-HD70",
            },
            {
              gpm: 44.5,
              id: "F-HD59",
            },
            {
              gpm: 42.5,
              id: "B-HD137",
            },
            {
              gpm: 42.75,
              id: "E-HD72",
            },
            {
              gpm: 41.25,
              id: "E-HD64",
            },
            {
              gpm: 40,
              id: "C-HD102",
            },
            {
              gpm: 39.25,
              id: "E-HD158",
            },
            {
              gpm: 39.5,
              id: "E-HD06",
            },
            {
              gpm: 38.25,
              id: "F-HD60",
            },
            {
              gpm: 36,
              id: "E-HD77",
            },
            {
              gpm: 35,
              id: "D-HD108",
            },
            {
              gpm: 33.75,
              id: "E-HD154",
            },
            {
              gpm: 25.75,
              id: "C-HD114",
            },
            {
              gpm: 25.75,
              id: "D-HD80",
            },
            {
              gpm: 22,
              id: "B-HD135",
            },
            {
              gpm: 21.5,
              id: "C-HD113",
            },
          ],
          valves_number: " 21",
        },
        {
          id: " 1",
          pump_works: " 2/2",
          total_gpm: " 1225.25",
          valves: [
            {
              gpm: 77.75,
              id: "E-HD74",
            },
            {
              gpm: 76.5,
              id: "E-HD61",
            },
            {
              gpm: 74.25,
              id: "E-HD62",
            },
            {
              gpm: 75,
              id: "E-HD65",
            },
            {
              gpm: 75,
              id: "E-HD67",
            },
            {
              gpm: 74.5,
              id: "E-HD73",
            },
            {
              gpm: 71.5,
              id: "E-HD66",
            },
            {
              gpm: 71.5,
              id: "E-HD78",
            },
            {
              gpm: 69.25,
              id: "B-HD150",
            },
            {
              gpm: 68.75,
              id: "E-HD156",
            },
            {
              gpm: 66.5,
              id: "E-HD157",
            },
            {
              gpm: 66,
              id: "E-HD69",
            },
            {
              gpm: 65,
              id: "E-HD79",
            },
            {
              gpm: 62,
              id: "C-HD101",
            },
            {
              gpm: 61.5,
              id: "E-HD75",
            },
            {
              gpm: 59.75,
              id: "E-HD155",
            },
            {
              gpm: 56,
              id: "E-HD76",
            },
            {
              gpm: 54.5,
              id: "B-HD149",
            },
          ],
          valves_number: " 18",
        },
      ],
      total_gpm: 2046.25,
      total_num_valves: 39,
    },
    {
      group_id: "LD",
      groups: [
        {
          id: " 0",
          pump_works: " 1/2",
          total_gpm: " 262.25",
          valves: [
            {
              gpm: 58.75,
              id: "F-LD56",
            },
            {
              gpm: 56,
              id: "F-LD54",
            },
            {
              gpm: 53.5,
              id: "F-LD55",
            },
            {
              gpm: 52.75,
              id: "F-LD57",
            },
            {
              gpm: 41.25,
              id: "F-LD58",
            },
          ],
          valves_number: " 5",
        },
      ],
      total_gpm: 262.25,
      total_num_valves: 5,
    },
    {
      group_id: "R",
      groups: [
        {
          id: " 0",
          pump_works: " 1/2",
          total_gpm: " 482.63",
          valves: [
            {
              gpm: 64.3,
              id: "E-R11",
            },
            {
              gpm: 61.19,
              id: "C-R10",
            },
            {
              gpm: 45.08,
              id: "C-R09",
            },
            {
              gpm: 37.81,
              id: "B-R05",
            },
            {
              gpm: 34.38,
              id: "E-R02",
            },
            {
              gpm: 33.99,
              id: "B-R16",
            },
            {
              gpm: 30.99,
              id: "B-R07",
            },
            {
              gpm: 26.72,
              id: "C-R08",
            },
            {
              gpm: 24.39,
              id: "E-R17",
            },
            {
              gpm: 22.27,
              id: "B-R06",
            },
            {
              gpm: 20.24,
              id: "E-R15",
            },
            {
              gpm: 16.31,
              id: "E-R12",
            },
            {
              gpm: 16.16,
              id: "E-R13",
            },
            {
              gpm: 15.32,
              id: "E-R01",
            },
            {
              gpm: 13.91,
              id: "E-R03",
            },
            {
              gpm: 10.99,
              id: "C-R04",
            },
            {
              gpm: 8.58,
              id: "E-R14",
            },
          ],
          valves_number: " 17",
        },
      ],
      total_gpm: 482.63000000000005,
      total_num_valves: 17,
    },
    {
      group_id: "MD",
      groups: [
        {
          id: " 0",
          pump_works: " 2/3",
          total_gpm: " 476.5",
          valves: [
            {
              gpm: 27.5,
              id: "A-MD13",
            },
            {
              gpm: 27.5,
              id: "B-MD144",
            },
            {
              gpm: 28,
              id: "C-MD05",
            },
            {
              gpm: 26.25,
              id: "A-MD39",
            },
            {
              gpm: 25.25,
              id: "B-MD41",
            },
            {
              gpm: 25.75,
              id: "B-MD128",
            },
            {
              gpm: 24.25,
              id: "A-MD19",
            },
            {
              gpm: 24.5,
              id: "A-MD21",
            },
            {
              gpm: 24,
              id: "A-MD34",
            },
            {
              gpm: 24,
              id: "B-MD138",
            },
            {
              gpm: 23.75,
              id: "D-MD89",
            },
            {
              gpm: 21.25,
              id: "A-MD29",
            },
            {
              gpm: 20,
              id: "B-MD40",
            },
            {
              gpm: 20,
              id: "B-MD148",
            },
            {
              gpm: 18.75,
              id: "D-MD123",
            },
            {
              gpm: 17.25,
              id: "C-MD98",
            },
            {
              gpm: 18,
              id: "D-MD85",
            },
            {
              gpm: 15.75,
              id: "A-MD153",
            },
            {
              gpm: 15.5,
              id: "C-MD97",
            },
            {
              gpm: 14.5,
              id: "B-MD43",
            },
            {
              gpm: 12.75,
              id: "A-MD37",
            },
            {
              gpm: 12,
              id: "C-MD104",
            },
            {
              gpm: 10,
              id: "D-MD107",
            },
          ],
          valves_number: " 23",
        },
        {
          id: " 1",
          pump_works: " 2/3",
          total_gpm: " 801.75",
          valves: [
            {
              gpm: 43.25,
              id: "B-MD51",
            },
            {
              gpm: 43.5,
              id: "D-MD124",
            },
            {
              gpm: 39,
              id: "A-MD15",
            },
            {
              gpm: 39,
              id: "A-MD17",
            },
            {
              gpm: 38.25,
              id: "C-MD116",
            },
            {
              gpm: 37.25,
              id: "A-MD26",
            },
            {
              gpm: 37.75,
              id: "B-MD130",
            },
            {
              gpm: 36.75,
              id: "B-MD136",
            },
            {
              gpm: 36.5,
              id: "B-MD139",
            },
            {
              gpm: 37,
              id: "D-MD83",
            },
            {
              gpm: 35.75,
              id: "B-MD52",
            },
            {
              gpm: 35,
              id: "B-MD49",
            },
            {
              gpm: 34,
              id: "B-MD47",
            },
            {
              gpm: 33.75,
              id: "D-MD84",
            },
            {
              gpm: 32.25,
              id: "D-MD92",
            },
            {
              gpm: 32.5,
              id: "D-MD93",
            },
            {
              gpm: 30.75,
              id: "A-MD35",
            },
            {
              gpm: 31,
              id: "B-MD143",
            },
            {
              gpm: 30.5,
              id: "C-MD04",
            },
            {
              gpm: 30.5,
              id: "D-MD95",
            },
            {
              gpm: 29.5,
              id: "B-MD133",
            },
            {
              gpm: 29.75,
              id: "C-MD07",
            },
            {
              gpm: 28.25,
              id: "B-MD48",
            },
          ],
          valves_number: " 23",
        },
        {
          id: " 2",
          pump_works: " 3/3",
          total_gpm: " 1096.75",
          valves: [
            {
              gpm: 53.75,
              id: "A-MD36",
            },
            {
              gpm: 53.5,
              id: "D-MD127",
            },
            {
              gpm: 51.75,
              id: "A-MD31",
            },
            {
              gpm: 50.5,
              id: "A-MD28",
            },
            {
              gpm: 50.25,
              id: "B-MD50",
            },
            {
              gpm: 50.75,
              id: "C-MD03",
            },
            {
              gpm: 49.25,
              id: "B-MD142",
            },
            {
              gpm: 48.25,
              id: "B-MD131",
            },
            {
              gpm: 48.25,
              id: "C-MD02",
            },
            {
              gpm: 47.25,
              id: "D-MD86",
            },
            {
              gpm: 48,
              id: "D-MD126",
            },
            {
              gpm: 47,
              id: "A-MD14",
            },
            {
              gpm: 46.25,
              id: "A-MD25",
            },
            {
              gpm: 46.75,
              id: "C-MD46",
            },
            {
              gpm: 46,
              id: "A-MD10",
            },
            {
              gpm: 45.75,
              id: "A-MD32",
            },
            {
              gpm: 46,
              id: "B-MD53",
            },
            {
              gpm: 45.5,
              id: "D-MD87",
            },
            {
              gpm: 45,
              id: "B-MD44",
            },
            {
              gpm: 44.25,
              id: "B-MD146",
            },
            {
              gpm: 44.5,
              id: "B-MD147",
            },
            {
              gpm: 44.5,
              id: "C-MD111",
            },
            {
              gpm: 43.75,
              id: "B-MD42",
            },
          ],
          valves_number: " 23",
        },
        {
          id: " 3",
          pump_works: " 3/3",
          total_gpm: " 1261.25",
          valves: [
            {
              gpm: 66,
              id: "A-MD11",
            },
            {
              gpm: 65.5,
              id: "A-MD20",
            },
            {
              gpm: 64.5,
              id: "A-MD33",
            },
            {
              gpm: 62.75,
              id: "A-MD12",
            },
            {
              gpm: 62.5,
              id: "D-MD90",
            },
            {
              gpm: 62.75,
              id: "D-MD118",
            },
            {
              gpm: 63,
              id: "D-MD125",
            },
            {
              gpm: 61.25,
              id: "C-MD99",
            },
            {
              gpm: 60.5,
              id: "C-MD96",
            },
            {
              gpm: 60.25,
              id: "D-MD94",
            },
            {
              gpm: 60.75,
              id: "E-MD81",
            },
            {
              gpm: 59.25,
              id: "A-MD38",
            },
            {
              gpm: 59.75,
              id: "B-MD145",
            },
            {
              gpm: 58.5,
              id: "C-MD06",
            },
            {
              gpm: 58.5,
              id: "D-MD119",
            },
            {
              gpm: 57,
              id: "A-MD23",
            },
            {
              gpm: 56.5,
              id: "B-MD129",
            },
            {
              gpm: 56.5,
              id: "D-MD82",
            },
            {
              gpm: 55.75,
              id: "D-MD91",
            },
            {
              gpm: 55,
              id: "B-MD140",
            },
            {
              gpm: 54.75,
              id: "C-MD106",
            },
          ],
          valves_number: " 21",
        },
        {
          id: " 4",
          pump_works: " 3/3",
          total_gpm: " 1244.75",
          valves: [
            {
              gpm: 76.25,
              id: "A-MD22",
            },
            {
              gpm: 76.25,
              id: "D-MD88",
            },
            {
              gpm: 76.25,
              id: "D-MD110",
            },
            {
              gpm: 77,
              id: "D-MD121",
            },
            {
              gpm: 74.25,
              id: "A-MD18",
            },
            {
              gpm: 74.75,
              id: "C-MD100",
            },
            {
              gpm: 74.5,
              id: "C-MD08",
            },
            {
              gpm: 75,
              id: "D-MD115",
            },
            {
              gpm: 73.25,
              id: "C-MD117",
            },
            {
              gpm: 72.25,
              id: "B-MD132",
            },
            {
              gpm: 72.75,
              id: "D-MD01",
            },
            {
              gpm: 72,
              id: "C-MD09",
            },
            {
              gpm: 72,
              id: "A-MD16",
            },
            {
              gpm: 72,
              id: "D-MD122",
            },
            {
              gpm: 70.75,
              id: "C-MD109",
            },
            {
              gpm: 69,
              id: "C-MD105",
            },
            {
              gpm: 66.5,
              id: "A-MD141",
            },
          ],
          valves_number: " 17",
        },
      ],
      total_gpm: 4881,
      total_num_valves: 107,
    },
  ];

  const [drawerIsOpened, setDrawerIsOpen] = React.useState(false);
  const [groups, setGroups] = React.useState<DataArray>(DUMMYDATA);
  const [showResult, setShowGroups] = React.useState<boolean>(false);

  const handleDrawerToggle = () => {
    setDrawerIsOpen((prevState) => !prevState);
  };

  const toggleShowResults = () => {
    setShowGroups((preState) => !preState);
  };

  return (
    <AppContext.Provider
      value={{
        drawerIsOpened,
        handleDrawerToggle,
        showResult,
        toggleShowResults,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error("useAppContext must be used within an AppWrapper");
  }
  return context;
}
