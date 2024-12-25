import streamlit as st
from streamlit import session_state as ss
import requests
import pandas as pd

#### Session state inicializations ####
if "update_machine_clicked_ID" not in ss: # for each machine holds the state of update process
    ss.update_machine_clicked_ID = ""

if "selected_filters" not in ss:
    ss.selected_filters = []


#### Functions ####
def updateMachine():
    # min length checks
    if len(ss["update_machine_clicked_name"]) <= 3:
        ss.backlog_message = "Machine name too short"
    else:
        # post update user info to API
        response = requests.post(
                        "http://10.21.31.5:40649/api/update/machine",
                        json={"ID":ss["update_machine_clicked_ID"], 
                        "name":ss["update_machine_clicked_name"],
                        "pnname":ss["update_machine_clicked_pnname"],
                        "chunkloaded":ss["update_machine_clicked_chunk_loaded"],
                        "note":ss["update_machine_clicked_note"]})
        data = response.json()
        ss["update_machine_clicked_ID"] = "" # reset edit state
        if data['status']:
            ss.backlog_message = "Machine updated"
        else:
            ss.backlog_message ="Failed to update machine"


#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.info(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Machines")

## select machines form ##
st.write("### List of machines")
response = requests.get("http://10.21.31.5:40649/api/get/machines")
if not response.json()["status"]:
    st.error("No machines, are your OC stations set up correctly?")
    st.stop()
df = pd.DataFrame(response.json()["machines"], columns=["ID", "Name", "Tier", "Amp", "Power Network", "Coord", "Chunk Loaded", "Operational", "Work Progress", "Created at", "OC Address", "Note"])

# Filters
filters = ["ID", "Name","Tier", "Amp", "Power Network", "Coord", "Chunk Loaded", "Operational", "Work Progress", "Created at", "OC Address", "Note"] 
selected_filters = st.multiselect("Select column filters", filters, default=ss["selected_filters"])
if selected_filters != ss["selected_filters"]: # update only on change
    ss["selected_filters"] = selected_filters
    st.rerun()

# List of machines container
if ss["selected_filters"]:
    # headers
    cols = st.columns(len(ss["selected_filters"]))
    for col, filter_name in zip(cols, ss["selected_filters"]):
        col.write(filter_name)
    
    # rows
    for _ , row in df.iterrows(): # iterate throught entries
        cols = st.columns(len(ss["selected_filters"])) # creates columns based on the number of filters
        for col, filter_name in zip(cols, ss["selected_filters"]): # zip maps values to eachother 
            col.write(row[filter_name])

        # Edit button logic
        if st.button(label="Edit", key=f"edit_{row["ID"]}"): # needs unique key
            ss["update_machine_clicked_ID"] = row["ID"] # sets the machine to be edited in dataframe
            # ss["delete_user_clicked_username"] = "" # resets delete state
            st.rerun()
        # Edit row logic 
        if ss["update_machine_clicked_ID"] == row["ID"]:
            # get power networks list
            response = requests.get("http://10.21.31.5:40649/api/get/power-network-names")
            if response.json()["status"]:
                power_networks = response.json()["pnnames"]
                power_networks.insert(0, None) # insert Null option
            else:
                power_networks = [None]

            # update form
            with st.form("update_form", border=False, enter_to_submit=False):
                submit_name = st.text_input(
                    "Custom Machine Name",
                    max_chars=100,
                    value=row["Name"],
                    key="update_machine_clicked_name" # holds value in session state beacuse buttons are stateless (smh)
                )
                submit_power_network_name = st.selectbox(
                    "Select Power Network", 
                    power_networks,
                    index=power_networks.index(row["Power Network"]),
                    key="update_machine_clicked_pnname"
                )
                submit_chunck_loaded = st.toggle(
                    "Chunk loaded",
                    value=row["Chunk Loaded"],
                    key="update_machine_clicked_chunk_loaded"
                )
                submit_note = st.text_input(
                    "Note", 
                    value=row["Note"],
                    key="update_machine_clicked_note"
                )
                if st.form_submit_button("Confirm changes"):
                    updateMachine()
                    st.rerun()
        st.divider()
else:
    st.write("No filters selected")
