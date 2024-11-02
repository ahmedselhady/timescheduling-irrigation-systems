
from pandas import DataFrame, read_csv, read_excel, ExcelWriter
from math import ceil
import io

class Utils:

    def __init__(self) -> None:
        pass

    @classmethod
    def num_to_col(cls, num):
        if num < 1:
            raise ValueError("num must be >= 1")
        result = ""
        while num:
            num, rem = divmod(num - 1, 26)
            result = chr(ord("A") + rem) + result
        return result
    
    @classmethod
    def get_pump_type(cls, data_table: DataFrame, pump_unit_gpm: float): 
        TWIN_PUMP = 2
        TRIPLET_PUMP = 3

        data_table["gpm_int"] = data_table["gpm"].apply(lambda x: ceil(x))

        data_table["valve_type_key"] = data_table.Valve.astype(str).apply(
            lambda x: x.strip().split("-")[-1][0]
        )

        twin_pump_decimals = [0, 1, 2, 4, 5, 8, 9]
        triplet_pump_decimals = [3, 7]
        total_valves_gpm = data_table.gpm_int.sum()
        num_batches = max(round(total_valves_gpm / pump_unit_gpm, 1), 1)
        pump_type = (
            TWIN_PUMP
            if (num_batches - int(num_batches)) * 10 in twin_pump_decimals
            else TRIPLET_PUMP
        )

        if pump_type == 2:
                pump_type_value = "TWIN"
        else:
            pump_type_value = "Triplet"

        return pump_type, pump_type_value
    
    @classmethod
    def read_datafile_as_dataframe(cls, uploaded_file):
        file_type = uploaded_file.name.split(".")[-1]
        file_type = uploaded_file.name.split(".")[-1]
        if file_type == "xlsx":
            data = read_excel(uploaded_file, header=0)
            data = data.rename(columns={"GPM": "gpm"})
        elif file_type == "txt":
            data = read_csv(uploaded_file, sep="\t")
            data = data.rename(columns={"AA": "Valve", "20": "gpm"})
        else:
            data = None

        return data  
    
    


    @classmethod
    def to_excel(cls, df:DataFrame) -> bytes:
        output = io.BytesIO()
        writer = ExcelWriter(output, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Sheet1", index=False, header=None)
        writer.close()
        processed_data = output.getvalue()
        return processed_data      