import yaml
import pandas as pd
import streamlit as st
import streamlit_ext as ste
from utils import Utils as ut
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from model.time_scheduling import TimeSchedulingAlgorithm as tsa


st.set_page_config(page_title="Time Scheduling", layout="wide")


data_frames = []

form_app = st.form("GPM Valve Grouping Algorithm")


with open('./assets/secrets/credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config.get('preauthorized', None)
)

name, authentication_status, username = authenticator.login( 'sidebar')

if authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.image('./assets/imgs/schedule.jpeg', use_column_width="auto")

else:

    nav_bar = st.columns(4)
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(location="sidebar",preauthorization=False)
        if email_of_registered_user:
            st.success('User registered successfully')

    except Exception as e:
        st.error(e)

    nav_bar[3] = authenticator.logout(location='sidebar')

    with form_app:

        st.write("Configurations:")

        uploaded_file = st.file_uploader("Choose a file")
        pump_unit_estimated_gpm = st.number_input("Pump Unit Estimated GPM")

        checkbox_columns = st.columns(7)

        allow_undersampling = checkbox_columns[0].checkbox("Accept 10% lower")
        allow_exact = checkbox_columns[1].checkbox("Accept exact GPM", value=True)
        allow_oversampling = checkbox_columns[2].checkbox("Accept 10% higher")

        submitted = st.form_submit_button("Calculate")

        if submitted:

            # * Make Summary pannel
            placeholder_cols = st.columns(4)
            total_num_batches_placeholder = placeholder_cols[0].empty()
            pump_type_placeholder = placeholder_cols[1].empty()
            avg_batch_gpm = placeholder_cols[2].empty()
            dummy = placeholder_cols[3].empty()

            st.divider()

            if len(data_frames) > 0:
                for x in data_frames:
                    del x
                data_frames = []

            if uploaded_file is not None and pump_unit_estimated_gpm is not None:

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
                    data_frames.append(new_df)
                    st.divider()


    if len(data_frames) > 0:

        csv = pd.concat(data_frames)
        ste.download_button(
            label="Export groups data as Excel",
            data=ut.to_excel(csv),
            file_name="schedule.xlsx",
            mime="application/vnd.ms-excel",
        )
