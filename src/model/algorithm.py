from utils import Utils as ut
from model.time_scheduling import TimeSchedulingAlgorithm as tsa
from pprint import pprint
from constants import network_type_map
import json

"""
uploaded_file = "/home/ahmed/work/Freelance/Ammo Assem/timescheduling-irrigation-systems/data/New/NOTATION.txt"
pump_unit_estimated_gpm = 1305
allow_exact = True
allow_oversampling = False
allow_undersampling = False
"""


def irregation_scheduling_algorithm(
    uploaded_file: str,
    pump_unit_estimated_gpm: int,
    allow_exact=True,
    allow_oversampling=False,
    allow_undersampling=False,
):

    data = ut.read_datafile_as_dataframe_from_path(uploaded_file)
    print("Got data")
    pump_type, pump_type_name = ut.get_pump_type(data, pump_unit_estimated_gpm)
    valve_type_keys = data.valve_type_key.unique().tolist()
    print("finding best schedule")
    solution = tsa.find_best_scheduling(
        data,
        pump_unit_estimated_gpm,
        pump_type,
        allow_exact,
        allow_oversampling,
        allow_undersampling,
    )

    batch_data = []
    total_num_batches = 0
    for s_ in solution[0]:
        bd = []
        key_ = s_[0]

        network_total_gpm = 0
        for sol_dict, gid, batch_gpm in zip(s_[1], s_[2], s_[3]):
            bd.append(
                {
                    "batch_id": gid,
                    "batch_total_gpm": float(batch_gpm),
                    "controller_valves": sol_dict,
                }
            )
            total_num_batches += 1
            network_total_gpm += float(batch_gpm)

        batch_data.append(
            {
                "network": f"{network_type_map[key_]} Network",
                "batchs": bd,
                "network_total_gpm": network_total_gpm,
            }
        )

    response_dict = {
        "pump_type": pump_type,
        "total_num_batches": total_num_batches,
        "batch_data": batch_data,
    }
    return response_dict
