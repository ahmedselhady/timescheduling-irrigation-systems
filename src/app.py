import streamlit as st
from copy import copy
from tqdm import tqdm
import pandas as pd
import math

from st_aggrid import AgGrid, GridOptionsBuilder


st.set_page_config(page_title="GPM Grouping", layout="wide")



def knapsack(weights, values, capacity, max_items):
    n = len(weights)
    # Create a table to store the maximum values at each capacity and number of items
    capacity = math.ceil(capacity)
    max_items = math.ceil(max_items)
    dp = [[[0 for _ in range(capacity + 1)] for _ in range(max_items + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, max_items + 1):
            for w in range(1, capacity + 1):
                if weights[i - 1][0] <= w:
                    dp[i][j][w] = max(values[i - 1] + dp[i - 1][j - 1][w - weights[i - 1][0]], dp[i - 1][j][w])
                else:
                    dp[i][j][w] = dp[i - 1][j][w]

    # Find the selected items
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][max_items][w] != dp[i - 1][max_items][w]:
            selected_items.append(weights[i-1])
            w -= weights[i - 1][0]
            max_items -= 1

    return selected_items

def get_groups(valve_data):

    total_valves_gpm = valve_data.gpm_int.sum()
    total_num_valves = len(valve_data)
    num_batches = round(total_valves_gpm/pump_unit_estimated_gpm, 1)

    pump_type =  TWIN_PUMP if (num_batches - int(num_batches))*10 in twin_pump_decimals else TRIPLET_PUMP
    per_pump_gpm = pump_unit_estimated_gpm/pump_type

    #num_controllers_needed = math.ceil(len(valve_data)/controller_valves_capacity)
    num_batches = math.ceil(num_batches)
    batch_capacity = math.ceil( len(valve_data) / num_batches )

    values = [ 1 for _ in range(len(valve_data))]
    weights = list(zip(valve_data['gpm_int'].tolist(), valve_data['Valve'].tolist()))
    weights.sort(key=lambda x: x[0])


    all_groups = []
    for run_ in tqdm(range(num_batches)):

        group_ = knapsack(weights, values, pump_unit_estimated_gpm, batch_capacity)
        all_groups.append(copy(group_))
        for element in group_:
            weights.remove(element)
    
    inverted_groups = []
    for idx, group_ in enumerate(all_groups):


        interm_group = []
        for x in group_:
            
            if isinstance(data.loc[data['Valve'] == x[-1]]['gpm'].item(), list):

                interm_group.append(( x[-1], data.loc[data['Valve'] == x[-1]]['gpm'].item() ))
            else:
                interm_group.append(( x[-1], data.loc[data['Valve'] == x[-1]]['gpm'].item() ))
        group_ = interm_group
        names = [ x[0] for x in group_]
        values = [ x[1] for x in group_]

        group_total_gpm = sum(values)
        number_of_pumps_required = math.ceil(group_total_gpm/per_pump_gpm)

        inverted_groups.append((f"Group ID: {idx}", "", 
                                f"Group Total GPM: {group_total_gpm}",
                                 f"Pump Works: {number_of_pumps_required}/{pump_type}",
                                f"Number of Valves: {len(names)}"))
        inverted_groups.append(names)
        inverted_groups.append(values)

    return pd.DataFrame(inverted_groups).fillna("")




data_frames = []

with st.form("GPM Valve Grouping Algorithm"):

    st.write("Configurations:")

    uploaded_file = st.file_uploader("Choose a file")
    #controller_valves_capacity = st.number_input('Controller Valves Capacity')
    pump_unit_estimated_gpm = st.number_input('Pump Unit Estimated GPM')

    #file_type = st.radio(
    #"File Type",
    #["*Text*", "*Excel*"],
    #captions = ["output files from CAD", "excel "])


    submitted = st.form_submit_button("Calculate")
    if submitted:

        if len(data_frames)>0:
            for x in data_frames:
                del x
            data_frames = []

        if uploaded_file is not None and pump_unit_estimated_gpm is not None:

            file_type = uploaded_file.name.split(".")[-1]

            if file_type == "xlsx":
                data = pd.read_excel(uploaded_file, header=0)
                data = data.rename(columns= {
                    "GPM": "gpm"
                })
            elif file_type == "txt":

                data=pd.read_csv(uploaded_file, sep="\t")
                data = data.rename(columns ={
                    "AA": "Valve",
                    "20": "gpm"
                })
            
            TWIN_PUMP = 2
            TRIPLET_PUMP = 3

            twin_pump_decimals = [ 0, 1, 2, 4, 5, 8, 9 ]
            triplet_pump_decimals = [ 3, 7 ] 

            data['gpm_int'] = data['gpm'].apply(lambda x: math.ceil(x))

            data['valve_type_key'] = data.Valve.astype(str).apply(lambda x: x.strip().split('-')[-1][0])
            
            valve_type_keys = data.valve_type_key.unique().tolist()


            for key in valve_type_keys:



                per_key_valves = data.loc[data['valve_type_key'] == key][['Valve', 'gpm_int', 'gpm']]  
                st.subheader(f'Valves Group {key}, total GPM = {per_key_valves["gpm"].sum()}, number of valves = {len(per_key_valves["gpm"])}', divider='rainbow')
                df= get_groups(per_key_valves)

                data_frames.append(st.dataframe(df, use_container_width=True))
                st.divider()



