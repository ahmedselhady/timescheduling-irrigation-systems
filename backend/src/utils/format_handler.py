import re
import math

def extract_until_number(input_str):
    # Regular expression to match characters until the first number
    match = re.match(r"[A-Za-z\-]+", input_str)

    if match:
        return match.group(0).split("-")[-1]  # Split by '-' and get the last part
    return None

def convert_to_json(result):
    result_json = {"types": []}
    for res in result:
        result_json["types"].append(
            {"group_id": extract_until_number(res[0][1])}
        )  # retrieves the group id
        # result_json["groups"][-1]["num"] = 10
        result_json["types"][-1]["groups"] = []
        total_gpm = 0
        valves_number = 0
        for i in range(0, res.shape[1]):  # res.shape[1] is the number of columns
            # print(res[i])
            counter = 0
            for item in res[i]:
                if isinstance(item, str) and ":" in item:
                    item = item.strip().split(":")
                    if item[0] == "Group ID":
                        result_json["types"][-1]["groups"].append({"id": item[1]})
                        result_json["types"][-1]["groups"][math.floor(counter / 3)]["valves"] = []

                    if item[0] == "Group Total GPM":
                        result_json["types"][-1]["groups"][math.floor(counter / 3)]["total_gpm"] = item[1]

                    if item[0] == "Pump Works":
                        result_json["types"][-1]["groups"][math.floor(counter / 3)]["pump_works"] = item[1]

                    if item[0] == "Number of Valves":
                        result_json["types"][-1]["groups"][math.floor(counter / 3)]["valves_number"] = item[1]
                        valves_number += float(item[1])

                elif isinstance(item, str) and item != "":
                    result_json["types"][-1]["groups"][math.floor(counter / 3)]["valves"].append({"id": item})

                elif isinstance(item, (int, float)):
                    result_json["types"][-1]["groups"][math.floor(counter / 3)]["valves"][-1]["gpm"] = item
                    total_gpm += float(item)
                    # counter += 1

                counter += 1

                # print("counter is: " + str(counter))
                # print(item)

            result_json["types"][-1]["total_gpm"] = total_gpm
            result_json["types"][-1]["total_num_valves"] = valves_number
            # print("------------------------------------------------------------")


    return result_json