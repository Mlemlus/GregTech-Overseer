import re, requests
def parseIntialData(data): # Processes the recieved OC data to structured data
    tbl = {}

    # OC station
    try:
        if data["1"]["name"] == "computer":
            tbl[1]={
                "computer_oc_address" : data["1"]["oc_address"]
            }
    except Exception as e:
        return False, "Wrong data format: " + str(e)

    # Machines
    for i in range(2,len(data)+1):
        try:
            val = {}
            # Variables all GT machines have
            if "machine" in data[str(i)]:
                val["oc_address"] = data[str(i)]["machine"]["oc_address"]
                val["name"] = data[str(i)]["machine"]["name"]
                val["owner_name"] = data[str(i)]["machine"]["owner_name"]
                val["coords_x"] = data[str(i)]["machine"]["coords"]["1"]
                val["coords_y"] = data[str(i)]["machine"]["coords"]["2"]
                val["coords_z"] = data[str(i)]["machine"]["coords"]["3"]
                val["input_eu"] = data[str(i)]["machine"]["input_eu"]
                val["allowed_work"] = data[str(i)]["machine"]["allowed_work"]
            

            # Variables only "power_source" machines have
            if "power_source" in data[str(i)]:
                val["is_power_source"] = True
                val["output_voltage"] = data[str(i)]["power_source"]["output_voltage"]
                val["output_voltage_avg"] = data[str(i)]["power_source"]["output_voltage_avg"] 
                val["input_eu"] = data[str(i)]["power_source"]["output_voltage"] # generators dont have input, so we set the tier based on the output
                val["input_voltage_avg"] = data[str(i)]["power_source"]["input_voltage_avg"]
                val["eu_capacity"] = data[str(i)]["power_source"]["eu_capacity"] 
                val["eu_capacity_current"] = data[str(i)]["power_source"]["eu_capacity_current"] 
                val["output_amp"] = data[str(i)]["power_source"]["output_amp"]
            
            # Sensor info extraction
            if data[str(i)]["machine"]["sensor_info"] != '': # empty sensor_info
                if not val["name"].startswith("basicmachine"): # no need for info from singleblocks
                    val = val | parseSensorInfo(data[str(i)]["machine"]["sensor_info"]) # | merges two dictionaries

            # just some cleanup
            if val["input_eu"] == 0: # machine/generator without input, cant determine tier
                val["input_eu"] = 8 # so we just set it to LV and cry about it
            else:
                val["input_eu"], amp = nearestTier(val["input_eu"]) 
                val["amp"] = amp 
            tbl[i] = val # add the machine to the table
        except Exception as e:
            requests.post("http://10.21.31.5:40649/log",json={
                "text":f"data_parse.parseIntialData:{data[str(i)]["machine"]["name"]}: {e}"
            })
    return tbl

def nearestTier(val): # returns tier eu of the val
    if val == 0: return 0,0
    nearest = 8
    try:
        while(True):
            if val <= nearest:
                nearest = nearest / 4 if val != nearest else nearest
                multiplier = val // nearest
                break
            else:
                nearest = nearest * 4
    except Exception as e:
        requests.post("http://10.21.31.5:40649/log",json={
                "text":f"data_parse.nearestTier: Failed to find the nearest tier for {val}, err: {e}"
            })
        return 0,0
    return int(nearest), int(multiplier)

# i am scared to read below this comment
# Update: I am still scared
def parseSensorInfo(sensor_info): # Extracts what it can from sensor data (the info when you hover over a machine controller)
    parsed_data = {} # output
    # first get rid of the formatting characters
    # These are just color modifiers etc.
    unformatted_sensor_info = [] # "Clean" sensor data
    for _, row in sensor_info.items():
        if "§" in row:
            formatting_chars = {"§a","§c","§e","§l","§n","§r","§1","§2","§3","§4","§5","§9", ","} # Table of chars for regex pattern, "," for integers
            pattern = '|'.join(re.escape(char) for char in formatting_chars) # Creation of the regex pattern (just combines the formatting_chars with |)
            row = re.sub(pattern,'',row) # Replaces the formatting_chars in sensor row with empty space
            row = row.replace('§','') # for anything left that didnt have a number
        unformatted_sensor_info.append(row)

    # secondly, split the strings into keys and values
    tmp_key = None # Holds the name of the variable when its on two rows, GT++ have Stored Energy:\n  int/int
    for row in unformatted_sensor_info:
        try:
            if tmp_key: # get value for previous line key
                parsed_data = parsed_data | extractValue(tmp_key, row) # Adds to output
                tmp_key = None
                continue
            elif ":" in row:
                # Split at the first :
                key, value = row.split(":", 1)
                key = key.strip()  # remove whitespace around key
                if key in parsed_data: # duplicate data, probably sci values
                    continue
                elif value.strip() == "": # the funny key, next line value solution
                    tmp_key = key
                    continue
                else:
                    parsed_data = parsed_data | extractValue(key, row)
            else:
                # when its just info (or a random string with usefull info)
                if row == "No Maintenance issues": # Combustion Engine speciality
                    parsed_data["Problems"] = 0
                elif row == "Needs Maintenance":
                    parsed_data["Problems"] = 1
                else:
                    continue
        except Exception as e:
            requests.post("http://10.21.31.5:40649/log",json={
                "text":f"data_parse.parseSensorInfo: Failed parse line {row} in sensor_info : {e}"
            })
            continue

    return parsed_data

def extractValue(key, val): # takes values, returns dictionary to merge
    # regex patterns
    int_pattern = re.compile(r"(\d+)")
    float_pattern = re.compile(r"(\d+\.\d+)")
    output = {}

    # val with multiple parts aka " / "
    if " / " in val:
        parts = val.split(" / ")
        output[key] = []
        for part in parts:
            # get the integer or float from each part
            if match := int_pattern.search(part): # I love warlus
                output[key].append(int(match.group()))
            elif match := float_pattern.search(part): # this shouldn't ever happen but when in rome
                output[key].append(float(match.group()))
            else:
                output[key].append(part.strip()) # get the string and strip the whitespaces

    # line "Problems: int Efficiency: float %",
    elif "Problems" in key:
        problems_match = int_pattern.search(val)
        efficiency_match = float_pattern.search(val)
        if problems_match and efficiency_match:
            output["Problems"] = int(problems_match.group())
            output["Efficiency"] = float(efficiency_match.group())

    # line Max Energy Income: int EU/t(*2A) Tier: str"
    elif "Max Energy Income" in key:
        val = val.replace("*2A","") # useless info
        max_energy_income_match = int_pattern.search(val) # get that info
        output["input_eu"] = int(max_energy_income_match.group()) # store that sweet info

    # lines with normal key: val
    else:
        # Single val extraction (int, float, or string)
        if int_match := int_pattern.search(val):
            output[key] = int(int_match.group())
        elif float_match := float_pattern.search(val):
            output[key] = float(float_match.group())
        else:
            output[key] = str(val.strip())  # didn't match anything
    return output