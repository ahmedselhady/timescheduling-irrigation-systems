import math
from tqdm import tqdm
from model import knapsac
from copy import copy
import pandas as pd

def get_groups(valve_data, pump_unit_estimated_gpm, data):
    TWIN_PUMP = 2
    TRIPLET_PUMP = 3

    twin_pump_decimals = [0, 1, 2, 4, 5, 8, 9]
    triplet_pump_decimals = [3, 7]

    total_valves_gpm = valve_data.gpm_int.sum()
    total_num_valves = len(valve_data)
    num_batches = round(total_valves_gpm / pump_unit_estimated_gpm, 1)

    pump_type = (
        TWIN_PUMP
        if (num_batches - int(num_batches)) * 10 in twin_pump_decimals
        else TRIPLET_PUMP
    )
    per_pump_gpm = pump_unit_estimated_gpm / pump_type

    # num_controllers_needed = math.ceil(len(valve_data)/controller_valves_capacity)
    num_batches = math.ceil(num_batches)
    batch_capacity = math.ceil(len(valve_data) / num_batches)

    values = [1 for _ in range(len(valve_data))]
    weights = list(zip(valve_data["gpm_int"].tolist(), valve_data["Valve"].tolist()))
    weights.sort(key=lambda x: x[0])

    all_groups = []
    for run_ in tqdm(range(num_batches)):

        group_ = knapsac.knapsack(weights, values, pump_unit_estimated_gpm, batch_capacity)
        all_groups.append(copy(group_))
        for element in group_:
            weights.remove(element)

    inverted_groups = []
    for idx, group_ in enumerate(all_groups):

        interm_group = []
        for x in group_:

            if isinstance(data.loc[data["Valve"] == x[-1]]["gpm"].item(), list):

                interm_group.append(
                    (x[-1], data.loc[data["Valve"] == x[-1]]["gpm"].item())
                )
            else:
                interm_group.append(
                    (x[-1], data.loc[data["Valve"] == x[-1]]["gpm"].item())
                )
        group_ = interm_group
        names = [x[0] for x in group_]
        values = [x[1] for x in group_]

        group_total_gpm = sum(values)
        number_of_pumps_required = math.ceil(group_total_gpm / per_pump_gpm)

        inverted_groups.append(
            (
                f"Group ID: {idx}",
                "",
                f"Group Total GPM: {group_total_gpm}",
                f"Pump Works: {number_of_pumps_required}/{pump_type}",
                f"Number of Valves: {len(names)}",
            )
        )
        inverted_groups.append(names)
        inverted_groups.append(values)

    return pd.DataFrame(inverted_groups).fillna("")
