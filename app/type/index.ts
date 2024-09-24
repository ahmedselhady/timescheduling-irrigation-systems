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

// for the new response

export interface ValveData {
  [key: string]: [string, number][][];
}

export interface Batch {
  batch_id: number;
  batch_total_gpm: number;
  controller_valves: ValveData;
}

export interface NetworkData {
  network: string;
  batchs: Batch[];
  network_total_gpm: number;
}

export interface ResponseData {
  pump_type: number;
  total_num_batches: number;
  batch_data: NetworkData[];
}
