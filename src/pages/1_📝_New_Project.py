import pandas as pd
import streamlit as st
import streamlit_ext as ste
from utils import Utils as ut
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from model.time_scheduling import TimeSchedulingAlgorithm as tsa
from pathlib import Path
import shutil
from datetime import datetime
import plotly.express as px
import pickle as pkl
import numpy as np
import datetime
from constants import network_type_map, pump_type_map
from statistics import median_high
import os, re
from math import ceil

st.set_page_config(layout="wide", page_icon=":memo:")

data_frames = []



def add_commas(line, maxwidth):

    line = line.strip()
    if line[-1] == ",":
        line = line[:-1]
    num_commas = line.count(",")
    needed_commas = maxwidth - num_commas
    line = line + " ".join([","] * needed_commas)
    return line[:-1]


def float_to_minutes_seconds(float_val):
    minutes = int(float_val)
    seconds = int((float_val - minutes) * 60)
    return f"{minutes}:{seconds:02d}"


def save_projects(to_be_saved, title: str, pump_gpm: float, pump_type: int):

    print(f"Got title {title}")
    suggested_path = Path(__file__).parent.parent / "projects" / title.strip()
    modified_path = suggested_path
    idx = 1
    while Path.exists(Path(modified_path)):

        modified_path = str(suggested_path) + "_" + str(idx)
        idx += 1
    Path.mkdir(Path(modified_path))

    meta_data = open(f"{str(modified_path)}/metadata.txt", "w")

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    meta_data.write(f"{title}\n")
    meta_data.write(f"{dt_string}###{pump_gpm}###{pump_type}")
    meta_data.write("\n")

    try:
        for make in to_be_saved:
            file_name = make[0].split(",")[0]
            make[-1].to_csv(f"{str(modified_path)}/{file_name}.csv", index=False)
            meta_data.write(f"{file_name}.csv###{make[0]}")
            meta_data.write("\n")
            meta_data.write(f"{file_name}.csv###{make[1]}")
            meta_data.write("\n")

        st.toast(f"Project {title} was saved successfuly!", icon="😍")
    except:
        print("An error occurred")
        shutil.rmtree(Path(modified_path))


if st.session_state.get("authentication_status", False):

    with st.form("GPM Valve Grouping Algorithm") as form_app:

        st.header("New Time Scheduling Project", divider="rainbow")
        
        project_title = st.text_input("Project Title", placeholder="New Project")

        uploaded_file = st.file_uploader("Select Project File")

        st.subheader("Configurations:")
        
        pump_data_col1, pump_data_col2 = st.columns([1,1], gap="large")
        pump_unit_estimated_gpm = pump_data_col1.number_input("Pump Unit Estimated GPM")
        pump_type_input = pump_data_col2.selectbox("Pump Unit Type", ("Single", "Twin", "Triplet"), index=0)
        
        checkbox_columns = st.columns(7)
        allow_undersampling = checkbox_columns[0].checkbox("Accept 10% lower")
        allow_exact = checkbox_columns[1].checkbox("Accept exact GPM", value=True)
        allow_oversampling = checkbox_columns[2].checkbox("Accept 10% higher")
        should_recommend_gpm = checkbox_columns[3].checkbox(
            "Recommend Pump Unit GPM", value=True
        )

        with st.expander(":gear: **Advanced Configurations**") as exp:

            #
            runtime_col1, runtime_col2 = st.columns([1, 1], gap="large")

            for idx, network_key in enumerate(network_type_map.keys()):

                if idx % 2 == 0:
                    runtime_handler = runtime_col1
                else:
                    runtime_handler = runtime_col2

                runtime_handler.write(f"**{network_type_map[network_key]} Netwroks**")
                runtime_handler.number_input(
                    "Runtime (min.)",
                    min_value=1.0,
                    max_value=24.0 * 60.0,
                    value=20.0,
                    step=0.5,
                    key=f"{network_key}_runtime",
                )
                runtime_handler.selectbox(
                    "Maximum pump utilization",
                    ("100%", "75%", "50%", "25%"),
                    index=0,
                    key=f"{network_key}_gpm_util",
                )
                runtime_handler.divider()

        _, __, ___, c3 = st.columns([1, 1, 1, 1], gap="large")
        with c3:
            submitted = c3.form_submit_button("**:blue[Calculate]**")

        if submitted:

            # * Make Summary pannel
            placeholder_cols = st.columns(4)
            total_num_batches_placeholder = placeholder_cols[0].empty()
            pump_type_placeholder = placeholder_cols[1].empty()
            avg_batch_gpm = placeholder_cols[3].empty()
            recommended_gpm = placeholder_cols[2].empty()

            st.divider()

            plot_placeholder = st.empty()
            st.divider()

            if len(data_frames) > 0:
                for x in data_frames:
                    del x
                data_frames = []

            if project_title is None:
                st.warning("Please enter a valid project title!")
            elif uploaded_file is None:
                st.warning("Please enter a valid file {text/excel}")
            elif pump_unit_estimated_gpm is None:
                st.warning("Please enter a valid Pump GPM")
            elif (
                project_title is not None
                and uploaded_file is not None
                and pump_unit_estimated_gpm is not None
            ):

                data = ut.read_datafile_as_dataframe(uploaded_file)
                print("Got data")
                pump_type, pump_type_name = pump_type_map[pump_type_input], pump_type_input #ut.get_pump_type(   data, pump_unit_estimated_gpm)
                
                data["gpm_int"] = data["gpm"].apply(lambda x: ceil(x))
                data["valve_type_key"] = data.Valve.astype(str).apply( lambda x: x.strip().split("-")[-1][0])
                
                valve_type_keys = data.valve_type_key.unique().tolist()
                print("finding best schedule")
                solution = tsa.find_best_scheduling(
                    data,
                    pump_unit_estimated_gpm,
                    pump_type,
                    allow_exact,
                    allow_oversampling,
                    allow_undersampling,
                    st.session_state.to_dict()
                )
                print("got solution")

                total_num_batches_placeholder.metric(
                    label="Total Number of Batches", value=solution[-1]
                )
                pump_type_placeholder.metric(label="Pump Type", value=pump_type_name)

                batch_values = []

                for newtork in solution[0]:

                    key, controller_cell_spans, network_header, newtork_solution = (
                        newtork
                    )

                    builder = GridOptionsBuilder.from_dataframe(newtork_solution)

                    ##* prepare column span values:
                    controller_cell_spans_string = ",".join(
                        [
                            f"'{k_}':{str(v_)}"
                            for k_, v_ in controller_cell_spans.items()
                        ]
                    )
                    controller_cell_spans_string = (
                        "{" + controller_cell_spans_string + " }"
                    )

                    for key in newtork_solution.columns:

                        configs = {
                            "field": key,
                            "minWidth": 5,
                        }
                        if key in ["A", "B", "C"]:
                            configs["pinned"] = "left"
                            configs["width"] = 110
                            configs["wrapText"] = True
                            configs["autoHeight"] = True

                        if key == "A":
                            rowspan_function = f"""
                                    function(params) {{
                                        if (typeof params.data.A === "string" && params.data.A.includes("Batch #")) {{
                                            return 2
                                        }} else {{
                                            return 1
                                        }}
                                    }};
                                """

                            configs["rowSpan"] = JsCode(rowspan_function)

                            configs["cellStyle"] = {
                                "color": "black",
                                "background-color": "#4ADEDE",
                            }

                        elif key == "B":
                            rowspan_function = f"""
                                    function(params) {{
                                        if (!isNaN(params.data.B)) {{
                                            return 2
                                        }} else {{
                                            return 1
                                        }}
                                    }};
                                """

                            # configs['rowSpan'] = JsCode(rowspan_function)

                            configs["cellStyle"] = {
                                "color": "black",
                                "background-color": "#797ef6",
                            }

                        elif key == "C":

                            configs["cellStyle"] = {
                                "color": "black",
                                "background-color": "#1aa7ec",
                            }

                        else:
                            configs["cellStyle"] = JsCode(
                                f"""
                                    function(params) {{
                                        if (isNaN(params.data.{key}) && typeof params.data.{key} === "string" && !params.data.{key}.includes("Controller")) {{
                                            return {{ 'color': 'black', 'font-weight':'bold', 'background-color': 'lightblue'}}
                                        }} else {{
                                            return {{ 'color': 'black'}}
                                        }}
                                    }};
                                """
                            )

                            #

                        colspan_function = f"""
                                    function(params) {{
                                        if (typeof params.data.{key} === "string" && params.data.{key}.includes("Controller")) {{
                                            let d_ = {controller_cell_spans_string};
                                            let parts = params.data.{key}.split(" ");
                                            let k_ = parts[parts.length-1];
                                            return d_[k_];
                                        }} else {{
                                            return 1
                                        }}
                                    }};
                                """

                        configs["colSpan"] = JsCode(colspan_function)

                        builder.configure_column(**configs)

                    go = builder.build()

                    rowstyle_code = JsCode(
                        """
                                    function(params) {
                                        if (params.data.A === 'Batch ID') {
                                            return {
                                                "font-weight":"bold",
                                                "text-align": "center",
                                                'backgroundColor': 'grey',
                                                'color': 'black',
                                                'font-size': "large"
                                            }
                                        }
                                    };
                                    """
                    )

                    go["getRowStyle"] = rowstyle_code
                    st.subheader(
                        network_header,
                        divider="rainbow",
                    )
                    grid_return = AgGrid(
                        newtork_solution, gridOptions=go, allow_unsafe_jscode=True
                    )
                    new_df = grid_return["data"]
                    data_frames.append(
                        (network_header, controller_cell_spans, newtork_solution)
                    )
                    st.divider()

                    for x in newtork_solution["C"].tolist()[1:]:

                        try:
                            x = float(x.strip())
                            batch_values.append(
                                (
                                    x,
                                    network_header.split(",")[0]
                                    .replace("Network", " ")
                                    .strip(),
                                )
                            )

                        except:
                            pass

                df = pd.DataFrame.from_records(
                    batch_values, columns=["Batch GPM", "Network"]
                )

                fig = px.scatter(df, y=df["Batch GPM"], color="Network")
                fig.update_traces(marker={"size": 15})
                for i in range(1, pump_type + 1):

                    hline_val = pump_unit_estimated_gpm / pump_type * i
                    fig.add_hline(y=hline_val, line_dash="dash", line_color="grey")
                plot_placeholder.plotly_chart(
                    fig, theme="streamlit", use_container_width=True
                )

                ### --------------------------------------------------------- ###
                original_solution_numbatches = df.shape[0]
                if should_recommend_gpm and not allow_oversampling:
                    alternative_solution = tsa.find_best_scheduling(
                        data,
                        pump_unit_estimated_gpm,
                        pump_type,
                        True,
                        True,
                        False,
                    )
                    print("got alternative solution")
                    batch_values = []

                    for newtork in solution[0]:

                        key, controller_cell_spans, network_header, newtork_solution = (
                            newtork
                        )

                        for x in newtork_solution["C"].tolist()[1:]:

                            try:
                                x = float(x.strip())
                                batch_values.append(
                                    (
                                        x,
                                        network_header.split(",")[0]
                                        .replace("Network", " ")
                                        .strip(),
                                    )
                                )

                            except:
                                pass

                    df = pd.DataFrame.from_records(
                        batch_values, columns=["Batch GPM", "Network"]
                    )

                    medhigh = int(median_high(df["Batch GPM"].tolist()))
                    if original_solution_numbatches >= df.shape[0]:
                        while medhigh <= pump_unit_estimated_gpm:
                            medhigh *= 1.05

                    recommended_gpm.metric(label="Recommended Pump GPM", value=medhigh)

                else:
                    recommended_gpm.metric(
                        label="Recommended Pump GPM", value=pump_unit_estimated_gpm
                    )

    if len(data_frames) > 0:

        csv = pd.concat([df[-1] for df in data_frames])
        dfs_combined = pd.concat(
            [data_frames[0][-1]] + [df_[-1].drop(index=0) for df_ in data_frames[1:]],
            ignore_index=True,
        )
        dfs_combined.drop(columns=["A", "B"], inplace=True)
        dfs_combined[dfs_combined.columns[:]].to_csv(
            "./check_format.csv", header=None, index=False
        )
        max_width = -999
        with open("./check_format.csv", "r") as f:
            compact_lines = ["Total GPM, Controllers ,"]
            for line_ in f.readlines()[1:]:
                compact_line = re.sub(",+", ",", line_)
                compact_lines.append(compact_line)
                if max_width < compact_line.count(","):
                    max_width = compact_line.count(",")
            compact_lines = [add_commas(cl, max_width) for cl in compact_lines]
            compact_lines = filter(
                lambda x: re.sub(",", "", x).strip() != "", compact_lines
            )
        with open("./check_format.csv", "w") as f:
            for i, cl in enumerate(compact_lines):
                f.write(cl)
                f.write("\n")
        dfs_combined = pd.read_csv(
            "./check_format.csv", header=None
        )
        os.remove("./check_format.csv")

        dfs_combined.fillna("", inplace=True)

        batch_gpms = dfs_combined[dfs_combined.columns[0]]

        valve_type = dfs_combined[dfs_combined.columns[4]].apply(
            lambda x: (
                network_type_map.get(
                    x.split("-")[-1][0].strip(), x.split("-")[-1][0].strip()
                )
                if "-" in str(x)
                else ""
            )
        )
        valve_type.iloc[0] = "Valve Type"

        temp_ = pd.concat((batch_gpms, valve_type), axis=1)
        
        total_gpd = temp_.apply(
            lambda x: (
                ""
                if (
                    x[temp_.columns[0]].strip() == ""
                    or "Total" in str(x[temp_.columns[0]])
                )
                else float(x[temp_.columns[0]])
                * st.session_state.get(f"{x[temp_.columns[1]].strip()[0]}_runtime", 20)
            ),
            axis=1,
        )
        total_gpd.iloc[0] = "Total GPD"
        gpm_permin = batch_gpms.apply(
            lambda x: "" if (x.strip() == "" or "Total" in x) else float(x)
        )
        gpm_permin.iloc[0] = "Total GPM"

        runtimes = valve_type.apply(
            lambda x: (
                ""
                if (x.strip() == "")
                else float_to_minutes_seconds(
                    st.session_state.get(f"{x.strip()[0]}_runtime", 20)
                )
            )
        )
        runtimes.iloc[0] = "Runtime (min)"

        time_from = []
        time_to = []
        indices = []
        init_time = datetime.datetime.strptime("06:00:00", "%H:%M:%S")
        batch_idx = 1
        for i in range(dfs_combined.shape[0]):

            if i % 2 == 0:
                time_from.append("")
                time_to.append("")
                indices.append("")
            else:
                time_from.append(init_time.strftime("%H:%M:%S"))
                init_time += datetime.timedelta(
                    minutes=st.session_state.get(
                        f"{valve_type.iloc[i].strip()[0]}_runtime", 20
                    )
                )
                time_to.append(init_time.strftime("%H:%M:%S"))
                indices.append(batch_idx)
                batch_idx += 1

        time_from[0] = "From"
        time_to[0] = "To"
        indices[0] = "Period"

        last_column_idx = dfs_combined.shape[-1] + 3
        dfs_combined = pd.concat((dfs_combined, runtimes), axis=1, ignore_index=True)
        last_column_idx += 1
        dfs_combined = pd.concat((dfs_combined, gpm_permin), axis=1, ignore_index=True)
        last_column_idx += 1
        dfs_combined = pd.concat((dfs_combined, total_gpd), axis=1, ignore_index=True)
        last_column_idx += 1
        dfs_combined.insert(0, ut.num_to_col(last_column_idx), valve_type)
        last_column_idx += 1
        dfs_combined.insert(0, ut.num_to_col(last_column_idx), time_to)
        last_column_idx += 1
        dfs_combined.insert(0, ut.num_to_col(last_column_idx), time_from)
        last_column_idx += 1
        dfs_combined.insert(0, ut.num_to_col(last_column_idx), indices)
        dfs_combined.drop(columns=dfs_combined.columns[4:5], axis=1, inplace=True)
        ste.download_button(
            label="Export groups data as Excel",
            data=ut.to_excel(dfs_combined),
            file_name="schedule.xlsx",
            mime="application/vnd.ms-excel",
        )

        st.button(
            "Save Project",
            on_click=save_projects,
            args=(data_frames, project_title, pump_unit_estimated_gpm, pump_type),
        )


else:
    st.switch_page("🏠_Home.py")
