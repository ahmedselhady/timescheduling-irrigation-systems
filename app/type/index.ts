export type Valve = {
  gpm: number;
  id: string;
};

export type Group = {
  id: string;
  pump_works: string;
  total_gpm: string | number;
  valves: Valve[];
  valves_number: string;
};

export type GroupCategory = {
  group_id: string;
  groups: Group[];
  total_gpm: number | string;
  total_num_valves: number;
};
