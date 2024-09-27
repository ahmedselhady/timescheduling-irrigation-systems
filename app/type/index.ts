// for the new response

interface ControllerValves {}

export interface Batch {
  batch_id: number;
  batch_total_gpm: number;
  controller_valves: ControllerValves;
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
