import re, sys 
def parseIntialData(data):
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
    count_mistakes = 0
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
            if val["input_eu"] == 0: # non-working machine/generator
                count_mistakes += 1
                raise ValueError('input_eu of machine is 0, skipping')
            else:
                val["input_eu"], amp = nearestTier(val["input_eu"]) 
                val["amp"] = amp 
            tbl[i - count_mistakes] = val # add the machine to the table

        except Exception as e:
            print(f"parseIntialData:{data[str(i)]["machine"]["name"]}: {e}",file=sys.stderr)

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
        print(f"data_parse: Failed to find the nearest tier for {val}, err: {e}", file=sys.stderr)
        return 0,0
    return int(nearest), int(multiplier)

# i am scared to read below this comment
def parseSensorInfo(sensor_info):
    parsed_data = {} # output

    # first get rid of the formatting characters
    unformatted_sensor_info = []
    for _, v in sensor_info.items():
        if "§" in v:
            formatting_chars = {"§a","§c","§e","§l","§n","§r","§1","§2","§3","§4","§5","§9", ","} # "," for integers
            pattern = '|'.join(re.escape(char) for char in formatting_chars)
            v = re.sub(pattern,'',v)
            v = v.replace('§','') # for anything left
        unformatted_sensor_info.append(v)
    
    # secondly, split the strings into keys and values
    tmp_key = None
    for v in unformatted_sensor_info:     
        try:
            if tmp_key: # get value for previous line key
                parsed_data = parsed_data | extractValue(tmp_key, v)
                tmp_key = None
                continue

            elif ":" in v:
                # Split at the first :
                key, value = v.split(":", 1)
                key = key.strip()  # remove whitespace around key
                if key in parsed_data: # duplicate data, probably sci values
                    continue
                elif value.strip() == "": # the funny key, next line value solution
                    tmp_key = key
                    continue
                else:
                    parsed_data = parsed_data | extractValue(key, v)

            else:
                # when its just info (or a random string with usefull info)
                if v == "No Maintenance issues": # Combustion Engine speciality
                    parsed_data["Problems"] = 0
                elif v == "Needs Maintenance":
                    parsed_data["Problems"] = 1
                else:
                    continue
        except Exception as e:
            print(f"parseSensorInfo: Can't parse line {v} in sensor_info : {e}", file=sys.stderr)
            continue

    return parsed_data

def extractValue(key, val): # takes values, returns dictionary to merge
    # regex patterns
    int_pattern = re.compile(r"(\d+)")
    float_pattern = re.compile(r"(\d+\.\d+)")\

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