import pandas as pd
import math
from model import get_groups

def parse_file(uploaded_file, pump_unit_estimated_gpm):
    data_frames = []
    if uploaded_file is not None and pump_unit_estimated_gpm is not None:

        file_type = uploaded_file.name.split(".")[-1]

        if file_type == "xlsx":
            data = pd.read_excel(uploaded_file, header=0)
            data = data.rename(columns={"GPM": "gpm"})
        elif file_type == "txt":

            data = pd.read_csv(uploaded_file, sep="\t")
            data = data.rename(columns={"AA": "Valve", "20": "gpm"})

        TWIN_PUMP = 2
        TRIPLET_PUMP = 3

        twin_pump_decimals = [0, 1, 2, 4, 5, 8, 9]
        triplet_pump_decimals = [3, 7]

        data["gpm_int"] = data["gpm"].apply(lambda x: math.ceil(x))

        data["valve_type_key"] = data.Valve.astype(str).apply(
            lambda x: x.strip().split("-")[-1][0]
        )

        valve_type_keys = data.valve_type_key.unique().tolist()

        for key in valve_type_keys:

            per_key_valves = data.loc[data["valve_type_key"] == key][
                ["Valve", "gpm_int", "gpm"]
            ]
            # st.subheader(
            #     f'Valves Group {key}, total GPM = {per_key_valves["gpm"].sum()}, number of valves = {len(per_key_valves["gpm"])}',
            #     divider="rainbow",
            # )
            df = get_groups.get_groups(per_key_valves, pump_unit_estimated_gpm, data)

            # data_frames.append(st.dataframe(df, use_container_width=True))
            data_frames.append(df)
            # st.divider()

    return data_frames
