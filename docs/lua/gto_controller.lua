-- GTOverseer controller
local internet = require("internet")
local component = require("component")
local computer = require("computer")
local term = require("term")
local event = require("event")
local server = "http://10.21.31.5:40649/data"

function toJSON(tbl)
    local result = '{'
    for k, v in pairs(tbl) do
        -- Add key
        result = result .. '"' .. tostring(k) .. '":'

        -- check if table to recursively call toJSON 
        if type(v) == "table" then
            result = result .. toJSON(v)
        -- check if string (value)
        elseif type(v) == "string" then
            result = result .. '"' .. v .. '"'
        -- if anything else (int/boolean) convert to string
        else
            result = result .. tostring(v)
        end

        result = result .. ','  -- add the , after value
    end
    if result:sub(-1) == ',' then
        result = result:sub(1, -2)-- remove the last ,
    end
    result = result .. '}'
    return result -- pray it works
end

function split (str, sep)
    local output = {}
    for val in str.gmatch(str, "([^"..sep.."]+)") do
       table.insert(output, val)
    end
    return output
 end

function postData(tbl)
    local body = toJSON(tbl)
    local response, status = internet.request(server, body, { ["Content-Type"] = "application/json" })

    if response then
        local response_body = ""
        for chunk in response do -- build the response from chunks
            response_body = response_body .. chunk
        end
        return response_body, status
    else
        return nil, status
    end
end

function reset()
    local oc_data = {}
    -- OC controller machine
    oc_data[1] = {
        name = "computer",
        oc_address = computer.address()
    }

    -- Iteration over GT machines
    for address in component.list("gt_machine") do
        local adapter = component.proxy(address) -- proxy address for interaction
        local machine_name = adapter.getName()
        if machine_name:sub(1,5) == "cable" or machine_name:sub(1,7) == "gt_pipe" then
            goto continue -- skip gt_machines that are not machines
        end
        local component_data = {}
        local sensor_info = ""
        if machine_name:sub(1,12) ~= "basicmachine" then
            sensor_info = (adapter.getSensorInformation and adapter.getSensorInformation()) or ""
        end

        component_data["machine"] = {
            oc_address = address,
            name = adapter.getName(),
            owner_name = adapter.getOwnerName(),
            coords = {adapter.getCoordinates()},
            sensor_info = sensor_info,
            input_eu = adapter.getInputVoltage(),
            allowed_work = adapter.isWorkAllowed()
        }

        -- the lapron cap, basic singleblock generators"
        if adapter.getName() == "multimachine.supercapacitor" or adapter.getName():sub(1,14) == "basicgenerator" then
            component_data["power_source"] = {
            output_voltage = adapter.getOutputVoltage(),
            output_voltage_avg = adapter.getAverageElectricOutput(),
            input_voltage_avg = adapter.getAverageElectricInput(),
            eu_capacity = adapter.getEUCapacityString(),
            eu_capacity_current = adapter.getStoredEUString(),
            output_amp = adapter.getOutputAmperage()
            }
        end

        -- Diesel generator
        if adapter.getName() == "multimachine.dieselengine" then
            component_data["power_source"] = {
            output_voltage = adapter.getOutputVoltage(),
            output_voltage_avg = adapter.getAverageElectricOutput(),
            input_voltage_avg = adapter.getAverageElectricInput(),
            eu_capacity = adapter.getEUCapacityString(),
            eu_capacity_current = adapter.getStoredEUString(),
            output_amp = adapter.getOutputAmperage()
            }
        end

        oc_data[#oc_data+1] = component_data
        ::continue::
    end

    -- Battery buffer
    for address in component.list("gt_batterybuffer") do
        local component_data = {}
        local adapter = component.proxy(address) -- proxy address for interaction
        local sensorInfo = (adapter.getSensorInformation and adapter.getSensorInformation()) or ""


        component_data["machine"] = {
            oc_address = address,
            name = adapter.getName(),
            owner_name = adapter.getOwnerName(),
            coords = adapter.getCoordinates(),
            sensor_info = sensorInfo,
            input_eu = adapter.getInputVoltage(),
            allowed_work = adapter.isWorkAllowed()
        }

        component_data["power_source"] = {
            output_amp = adapter.getOutputAmperage(),
            output_voltage = adapter.getOutputVoltage(),
            output_voltage_avg = adapter.getAverageElectricOutput(),
            input_voltage_avg = adapter.getAverageElectricInput()
        }

        oc_data[#oc_data+1] = component_data
    end
    print("Number of connected GT machines: " .. #oc_data)
    local data={}
    data["oc_address"] = computer.address()
    data["data"] = oc_data
    data["status"] = "205" -- 205 HTTP code to reset content 
    return data
end

function update(work_table) -- send work progress data if machine working
    local oc_data = {}

    -- Iteration over GT machines
    for address in component.list("gt_machine") do
        local adapter = component.proxy(address) -- proxy address for interaction
        local machine_name = adapter.getName()
        if machine_name:sub(1,5) == "cable" or machine_name:sub(1,7) == "gt_pipe" then
            goto continue -- skip gt_machines that are not machines
        end

        -- Check if machine is working
        if adapter.hasWork() then
            work_table[address] = true
            local component_data = { -- add machines work info to return data
                oc_address = address,
                work_progress = adapter.getWorkProgress(),
                work_progress_max = adapter.getWorkMaxProgress()
            }
            -- If it has power storage update value
            if adapter.getStoredEUString ~= nil then
                component_data["eu_capacity_current"] = adapter.getStoredEUString()
            end

            oc_data[#oc_data+1] = component_data
        end
        ::continue::
    end

    -- check if any machine stopped working
    for address, _ in pairs(work_table) do
        if component.proxy(address).hasWork() == false then
            local component_data = { -- return 0 values for non-working machines
            oc_address = address,
            work_progress = 0,
            work_progress_max = 0
            }
            oc_data[#oc_data+1] = component_data
            work_table[address] = nil -- remove the address from table
        end
    end

    if #oc_data == 0 then -- no working machines, no update
        return false
    end

    local data={}
    data["oc_address"] = computer.address()
    data["data"] = oc_data
    data["status"] = "100" -- 100 HTTP code to update data 
    return data
end

function configuration(conf_string)
    local conf = split(conf_string,",")
    update_rate = tonumber(conf[1]) -- remember kids, lua counts from 1!
    print("New update rate: " .. update_rate)
    local data={}
    data["oc_address"] = computer.address()
    data["status"] = "204" -- 100 HTTP code to update data
    return data
end

------- Inicialization -------
term.clear()
print("GregTech Overseer Controller")
print("To exit the program use CTRL + C")
print("Inicialization...")
update_rate = 1
local response = postData(reset())
local work_table = {} -- holds addresses of working machines
print("Finished inicialization")
------- Main loop -------
while true do
    local task = response:sub(1,3)
    if task == "100" then
        local upd_data = update(work_table)
        if upd_data then
            response = postData(upd_data)
        end
    elseif task == "205" then
        print("Updating connected machines list...")
        response = postData(reset())
        print("Connected machines list updated")
    elseif task == "204" then
        print("Recieved config update...")
        response = postData(configuration(response:sub(4,-1)))
        print("Finished config update")
    end


    -- break point if needed, also doubles as update rate
    if event.pull(update_rate, "interrupted") then
        term.clear()
        print("stopped")
        os.exit()
    end
end