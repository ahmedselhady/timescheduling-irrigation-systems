import streamlit as st
import os
from pathlib import Path
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import pandas as pd
import plotly.express as px
import shutil

st.set_page_config(page_icon="🖇", layout="wide")

def convert_metadata_to_dict(meta_data):
    dictionary = {}
    for idx in range(2, len(meta_data)):
        key = meta_data[idx].split("###")[0]
        if key not in dictionary:
            dictionary[key] = []
        dictionary[key].append(meta_data[idx].split("###")[-1])
    return dictionary

def delete_project(path:str, project_name:str):

    print(path)
    if os.path.exists(path) and first_click:
        shutil.rmtree(path)
        st.toast(f"Project {project_name} was deleted successfully!", icon="🚫")
    else:
        st.toast(f"Project {project_name} does not exist!", icon="⚠️")

first_click = False


if st.session_state.get("authentication_status", False):




    path = str(Path(__file__).parent.parent/"projects")

    key_id = 0

    
    projects_list = os.listdir(path)

    if len(projects_list) == 0:
        st.image(str(Path(__file__).parent.parent/"assets/imgs/empty.png"))

    for project in projects_list:
        
        meta_data = open(f"{path}/{project}/metadata.txt", 'r').readlines()

        creation_date= meta_data[1].split("###")[0]
        pump_gpm, pump_type = float(meta_data[1].split("###")[1]), int(meta_data[1].split("###")[2])

        expander_header= f"Project Name: {meta_data[0]}"

        with st.expander(expander_header):
            
            st.divider()
            cols = st.columns(3)
            cols[0].metric("Estimated Pump GPM", pump_gpm)
            cols[1].metric("Pump Type", 'Twin' if pump_type == 2 else 'Triplet', delta=f"{pump_gpm/pump_type} gpm each")
            cols[2].metric("Created at", creation_date.split()[0], delta=creation_date.split()[-1])
            st.divider()

            placeholder = st.empty()
            st.divider()

            networks = list(os.walk(f"{path}/{project}"))[0][-1]
            meta_data = convert_metadata_to_dict(meta_data)

            batch_values = []

            for newtork_solution_path in networks:
                
                if "metadata" in newtork_solution_path:
                    continue

                newtork_solution = pd.read_csv(f"{path}/{project}/{newtork_solution_path}", header=0)

                network_header, controller_cell_spans_string = meta_data[newtork_solution_path][0], meta_data[newtork_solution_path][1]

                for x in newtork_solution['C'].tolist()[1:]:
                    
                    try:
                        x = float(x.strip())
                        batch_values.append((x, network_header.split(",")[0].replace("Network", " ").strip()))
            
                    except:
                        pass
                builder = GridOptionsBuilder.from_dataframe(newtork_solution)

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
                    newtork_solution, gridOptions=go, allow_unsafe_jscode=True, key=key_id
                )
                key_id += 1
                #st.write(grid_return)

            df = pd.DataFrame.from_records(batch_values, columns=["Batch GPM", "Network"])
            fig = px.scatter(df, y=df['Batch GPM'], color="Network"  )
            fig.update_traces(marker={'size': 15})
            for i in range(1, pump_type+1):

                hline_val = pump_gpm/pump_type*i
                fig.add_hline(y=hline_val, line_dash="dash", line_color="grey")

            placeholder.plotly_chart(fig, theme="streamlit", use_container_width=True)

            cols = st.columns(4, gap='large')

            cols[3].button("Delete Project :wastebasket:", key=f'proj_{project}', on_click=delete_project, args=(str(path)+"/"+project, expander_header.split(':')[-1].strip()))

    first_click = True

else:
    st.switch_page("🏠_Home.py")


