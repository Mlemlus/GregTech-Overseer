import streamlit as st
from streamlit import session_state as ss
import requests
import pandas as pd

#### Session state inicializations ####
if "update_ps_clicked_machine_ID" not in ss: # for each power source holds the state of update process
    ss.update_ps_clicked_machine_ID = ""


#### Functions ####
def addPS():
    try:
        # post new ps info to API
        response = requests.post(
            "http://10.21.31.5:40649/api/add/power-source",
            json={
                "machine_ID": ss["add_ps_machine_ID"],
                "output_amp": ss["add_ps_output_amp"],
                "current_capacity":0,
                "max_capacity": ss["add_ps_max_capacity"],
                "manual": True
                })
        data = response.json()
        if data['status']: # returned status
            ss.backlog_message = "Power Source added"
        else:
            ss.backlog_message ="Failed to add power source"
    except Exception as e:
        ss.backlog_message = f"addPS error: {e}"


def updatePS():
    # min length checks
    if len(ss["update_ps_name"]) <= 1:
        ss.backlog_message = "Machine name too short"
    else:
        # post update ps info to API
        response = requests.post(
            "http://10.21.31.5:40649/api/update/power-source",
            json={
                "machine_ID":ss["update_ps_clicked_machine_ID"],
                "output_amp":ss["update_ps_output_amp"],
                "max_capacity":ss["update_ps_max_capacity"],
                "name":ss["update_ps_name"],
                "pnname":ss["update_ps_pnname"],
                "note":ss["update_ps_note"],
                "manual":True
                })
        data = response.json()
        ss["update_ps_clicked_machine_ID"] = "" # reset edit state
        if data['status']:
            ss.backlog_message = "Power Source updated"
        else:
            ss.backlog_message ="Failed to update power source"

def deletePS():
    # post delete ps info to API
    response = requests.post("http://10.21.31.5:40649/api/delete/power-source", json={"name":ss["delete_ps_clicked_machine_ID"]})
    data = response.json()
    ss["delete_ps_clicked_machine_ID"] = "" # reset delete state
    if data['status']:
        ss.backlog_message = "Power Source deleted"
    else:
        ss.backlog_message ="Failed to delete power source"


#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.toast(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Power Source Managment")

## select pss form ##
response = requests.get("http://10.21.31.5:40649/api/get/power-sources")
if response.json()["status"]:
    df = pd.DataFrame(response.json()["pss"], columns=["Name","Tier","Output Amp", "Power Network", "Cur. Capacity", "Max Capacity", "machine_ID", "manual"])
else:
    st.error(response.json()["pss"])
    st.stop()
if response.json()["pss"] == []:
    st.error("No Power Sources :(")

# List of pss container
with st.container(height=700):
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    col1.write("Name")
    col2.write("Tier")
    col3.write("Output Amp")
    col4.write("Power Network")
    col5.write("Cur. Capacity")
    col6.write("Max Capacity")
    col7.write("Manually set")
    for _ , row in df.iterrows(): # iterate throught entries
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
        col1.write(row["Name"])
        col2.write(row["Tier"])
        col3.write(row["Output Amp"])
        col4.write(row["Power Network"])
        col5.write(row["Cur. Capacity"])
        col6.write(row["Max Capacity"])
        col7.write(row["manual"])
        if not row["Name"] == '': # display buttons if we got any pss
            # Edit button logic
            if "Edit Power Source Machines" in ss.privileges or "Administrator" in ss.privileges:
                if col8.button(label="Edit", key=f"edit_{row["machine_ID"]}"): # needs unique key
                    ss["update_ps_clicked_machine_ID"] = row["machine_ID"] # sets the name to be edited in dataframe
                    ss["delete_ps_clicked_machine_ID"] = "" # resets delete state
                    st.rerun()

            # Edit row logic
            if ss["update_ps_clicked_machine_ID"] == row["machine_ID"]:
                # get power source details
                response = requests.post("http://10.21.31.5:40649/api/get/power-source", json={"machine_ID":row["machine_ID"]})
                if response.json()["status"]:
                    ps = response.json()["ps"]
                else: 
                    ps = [None]
                # get power networks list
                response = requests.get("http://10.21.31.5:40649/api/get/power-network-names")
                if response.json()["status"]:
                    power_networks = [i[0] for i in response.json()["pnnames"]]
                    power_networks.insert(0, None) # insert Null option
                else:
                    power_networks = [None]

                # update form
                with st.form("update_form", border=False, enter_to_submit=False):
                    st.text_input(
                        "Name",
                        max_chars=50,
                        value=ps[0],
                        key="update_ps_name"
                    )
                    st.number_input(
                        "Output Amp",
                        min_value=1,
                        max_value=65536,
                        step=1,
                        format="%d",
                        value=ps[1],
                        key="update_ps_output_amp"
                    )
                    st.number_input(
                        "Max Capacity",
                        min_value=1,
                        max_value=(1 << 53) - 1,
                        step=1,
                        format="%d",
                        value=ps[2],
                        key="update_ps_max_capacity"
                    )
                    st.selectbox(
                        "Select Power Network",
                        power_networks,
                        index=power_networks.index(row["Power Network"]),
                        key="update_ps_pnname"
                    )
                    st.text_input(
                    "Note", 
                    value=ps[3],
                    key="update_ps_note"
                )
                    st.form_submit_button("Confirm changes", on_click=updatePS)

            # Delete button logic
            # if row["manual"]: # only manually added PS can be deleted
            #     if col9.button(label="Delete", key=f"delete_{row["machine_ID"]}"): # needs unique key
            #         ss["delete_ps_clicked_machine_ID"] = row["machine_ID"] # sets the name to be delete in dataframe
            #         ss["update_ps_clicked_machine_ID"] = "" # Resets edit state
            #         st.rerun()
                
            #     # Delete row logic
            #     if ss["delete_ps_clicked_machine_ID"] == row["machine_ID"]:
            #         if st.button(f"Confirm deletion of {row['Name']}"):
            #             deletePS()
            #             st.rerun()


# Perhaps possible
# ## Add ps form ##
# st.write("### Add Power Network")
# # get cables list
# response = requests.get("http://10.21.31.5:40649/api/get/cable-names")
# if response.json()["status"]:
#     cables = [i[0] for i in response.json()["cables"]]
# else:
#     st.warning("No cables: First add some cables in the Utils/Cables tab")
#     st.stop()
# # Field inputs
# with st.form("uadd_form", border=False, enter_to_submit=False):
#     st.text_input(
#         "Name",
#         max_chars=50,
#         key="add_ps_name"
#     )
#     st.selectbox(
#         "Select Cable",
#         cables,
#         key="add_ps_cable_name"
#     )
#     st.form_submit_button("Add", on_click=addPS)