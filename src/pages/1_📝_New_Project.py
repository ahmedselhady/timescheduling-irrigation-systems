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

st.set_page_config(layout="wide", page_icon=":memo:")

data_frames = []


def save_projects(to_be_saved, title:str, pump_gpm:float, pump_type:int):
    
    print(f"Got title {title}")
    suggested_path = Path(__file__).parent.parent/"projects"/ title.strip()
    modified_path = suggested_path
    idx = 1
    while Path.exists(Path(modified_path)):

        modified_path = str(suggested_path) + '_' + str(idx)
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

        st.toast(f'Project {title} was saved successfuly!', icon='😍')  
    except:
        print("An error occurred")
        shutil.rmtree(Path(modified_path))

if st.session_state.get("authentication_status", False):

    with st.form("GPM Valve Grouping Algorithm") as form_app:

        project_title = st.text_input("Project Title")

        st.write("Configurations:")
        uploaded_file = st.file_uploader("Choose a file")
        pump_unit_estimated_gpm = st.number_input("Pump Unit Estimated GPM")

        checkbox_columns = st.columns(7)

        allow_undersampling = checkbox_columns[0].checkbox("Accept 10% lower")
        allow_exact = checkbox_columns[1].checkbox("Accept exact GPM", value=True)
        allow_oversampling = checkbox_columns[2].checkbox("Accept 10% higher")

        c1, c2, c3 = st.columns([1, 1, 1], gap="large")
        with c3:
            c3_1, c3_2 = st.columns([1, 1])
            with c3_2:
                submitted = st.form_submit_button("Calculate")
            
        if submitted:

            # * Make Summary pannel
            placeholder_cols = st.columns(4)
            total_num_batches_placeholder = placeholder_cols[0].empty()
            pump_type_placeholder = placeholder_cols[1].empty()
            avg_batch_gpm = placeholder_cols[2].empty()
            dummy = placeholder_cols[3].empty()
            
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
            elif project_title is not None and uploaded_file is not None and pump_unit_estimated_gpm is not None:

                data = ut.read_datafile_as_dataframe(uploaded_file)
                print("Got data")
                pump_type, pump_type_name = ut.get_pump_type(data, pump_unit_estimated_gpm)
                # per_pump_gpm = pump_unit_estimated_gpm / pump_type
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
                print("got solution")

                total_num_batches_placeholder.metric(
                    label="Total Number of Batches", value=solution[-1]
                )
                pump_type_placeholder.metric(label="Pump Type", value=pump_type_name)

                batch_values = []


                for newtork in solution[0]:

                    key, controller_cell_spans, network_header, newtork_solution = newtork

                    builder = GridOptionsBuilder.from_dataframe(newtork_solution)

                    ##* prepare column span values:
                    controller_cell_spans_string = ",".join(
                        [f"'{k_}':{str(v_)}" for k_, v_ in controller_cell_spans.items()]
                    )
                    controller_cell_spans_string = "{" + controller_cell_spans_string + " }"

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
                    data_frames.append((network_header,controller_cell_spans, newtork_solution))
                    st.divider()

                    for x in newtork_solution['C'].tolist()[1:]:
                    
                        try:
                            x = float(x.strip())
                            batch_values.append((x, network_header.split(",")[0].replace("Network", " ").strip()))
                
                        except:
                            pass


                df = pd.DataFrame.from_records(batch_values, columns=["Batch GPM", "Network"])
                
                fig = px.scatter(df, y=df['Batch GPM'], color="Network"  )
                fig.update_traces(marker={'size': 15})
                for i in range(1, pump_type+1):

                    hline_val = pump_unit_estimated_gpm/pump_type*i
                    fig.add_hline(y=hline_val, line_dash="dash", line_color="grey")
                plot_placeholder.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    if len(data_frames) > 0:

        
        csv = pd.concat([ df[-1] for df in data_frames])
        ste.download_button(
            label="Export groups data as Excel",
            data=ut.to_excel(csv),
            file_name="schedule.xlsx",
            mime="application/vnd.ms-excel",
        )

        st.button("Save Project", on_click=save_projects, args=(data_frames, project_title, pump_unit_estimated_gpm, pump_type))


else:
    st.switch_page("🏠_Home.py")


