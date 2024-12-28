import streamlit as st
from streamlit import session_state as ss
import requests
import pandas as pd

#### Session state inicializations ####
if "update_cable_old_name" not in ss: # holds the selected name of update process
    ss.update_cable_old_name = ""

if "delete_cable_name" not in ss:
    ss.delete_cable_name = ""


#### Functions ####
def addCable():
    try:
        if len(ss["add_cable_name"]) >= 1:
            # post new cable info to API
            response = requests.post(
                "http://10.21.31.5:40649/api/add/cable", 
                json={
                    "name": ss["add_cable_name"],
                    "density": ss["add_cable_density"],
                    "tier_name": ss["add_cable_tier_name"],
                    "max_amp": ss["add_cable_max_amp"],
                    "loss":ss["add_cable_loss"] # like the meme
                    })
            data = response.json()
            if data['status']: # returned status
                ss.backlog_message = "Cable added"
            else:
                ss.backlog_message = f"Failed to add cable: {data["error"]}"
        else:
            ss.backlog_message="Cable name too short"
    except Exception as e:
        ss.backlog_message = f"addCable error: {e}"


def updateCable():
    # min length checks
    if len(ss["update_cable_name"]) <= 1:
        ss.backlog_message = "Name too short"
    else:
        # post update cable info to API
        response = requests.post(
            "http://10.21.31.5:40649/api/update/cable",
            json={
                "old_name":ss["update_cable_old_name"],
                "name":ss["update_cable_name"],
                "density":ss["update_cable_density"],
                "tier_name":ss["update_cable_tier_name"],
                "max_amp":ss["update_cable_max_amp"],
                "loss":ss["update_cable_loss"]
                })
        data = response.json()
        ss["update_cable_old_name"] = "" # reset edit state
        if data['status']:
            ss.backlog_message = "Cable updated"
        else:
            ss.backlog_message ="Failed to update cable"

def deleteCable():
    # post delete cable info to API
    response = requests.post("http://10.21.31.5:40649/api/delete/cable", json={"name":ss["delete_cable_name"]})
    data = response.json()
    ss["delete_cable_name"] = "" # reset delete state
    if data['status']:
        ss.backlog_message = "Cable deleted"
    else:
        ss.backlog_message = f"Failed to delete cable: {data["error"]}"


#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.toast(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Cable Managment")

## select cables form ##
response = requests.get("http://10.21.31.5:40649/api/get/cables")
if not response.json()["status"]:
    st.error("No cables :(")
    df = pd.DataFrame([['']*5], columns=["Name","Tier","Density", "Max Amp", "Loss"])
else:
    df = pd.DataFrame(response.json()["cables"], columns=["Name","Tier","Density", "Max Amp", "Loss"])

# List of cables container
with st.container(height=600):
    col1, col2, col3, col4, col5, col6, col7 = st.columns([4, 1, 1.5, 1, 1.5, 2, 2])
    col1.write("Name")
    col2.write("Tier")
    col3.write("Density")
    col4.write("Amp")
    col5.markdown("Loss", help="~~:.|:;~~")
    for _ , row in df.iterrows(): # iterate throught entries
        col1, col2, col3, col4, col5, col6, col7 = st.columns([4, 1, 1, 1, 1, 2, 2]) # maybe I should declare differently
        col1.write(row["Name"])
        col2.write(row["Tier"])
        col3.write(row["Density"])
        col4.write(row["Max Amp"])
        col5.write(row["Loss"])

        if not row["Name"] == '': # display buttons if we got any cables
            # Edit button logic
            if "Edit Cables" in ss.privileges or "Administrator" in ss.privileges:
                if col6.button(label="Edit", key=f"edit_{row["Name"]}"): # needs unique key
                    ss["update_cable_old_name"] = row["Name"] # sets the name to be edited in dataframe
                    ss["delete_cable_name"] = "" # resets delete state
                    st.rerun()

            # Edit row logic
            if ss["update_cable_old_name"] == row["Name"]:
                # get tiers list
                response = requests.get("http://10.21.31.5:40649/api/get/tier-names")
                if response.json()["status"]:
                    tiers = [i[0] for i in response.json()["tiers"]]
                else:
                    st.warning("No tiers: No connection to the database or your databse is corrupt")
                    st.stop()

                # update form
                with st.form("update_form", border=False, enter_to_submit=False):
                    st.text_input(
                        "Name",
                        max_chars=50,
                        value=row["Name"],
                        key="update_cable_name"
                    )
                    st.selectbox(
                        "Select Tier",
                        tiers,
                        index=tiers.index(row["Tier"]),
                        key="update_cable_tier_name"
                    )
                    st.number_input(
                        "Density",
                        min_value=1,
                        max_value=65536,
                        step=1,
                        format="%d",
                        value=row["Density"],
                        key="update_cable_density"
                    )
                    st.number_input(
                        "Max Amp",
                        min_value=1,
                        max_value=65536,
                        step=1,
                        format="%d",
                        value=row["Max Amp"],
                        key="update_cable_max_amp"
                    )
                    st.number_input(
                        "Power Loss",
                        min_value=0,
                        max_value=65536,
                        step=1,
                        format="%d",
                        value=row["Loss"],
                        key="update_cable_loss"
                    )
                    st.form_submit_button("Confirm changes", on_click=updateCable)

            # Delete button logic
            if "Remove Cables" in ss.privileges or "Administrator" in ss.privileges:
                if col7.button(label="Delete", key=f"delete_{row["Name"]}"): # needs unique key
                    ss["delete_cable_name"] = row["Name"] # sets the name to be delete in dataframe
                    ss["update_cable_old_name"] = "" # Resets edit state
                    st.rerun()

            # Delete row logic
            if ss["delete_cable_name"] == row["Name"]:
                if st.button(f"Confirm deletion of {row['Name']}"):
                    deleteCable()
                    st.rerun()


if "Add Cables" in ss.privileges or "Administrator" in ss.privileges:
    ## Add cable form ##
    with st.expander("Add Cable"):
        # get tiers list
        response = requests.get("http://10.21.31.5:40649/api/get/tier-names")
        if response.json()["status"]:
            tiers = [i[0] for i in response.json()["tiers"]]
        else:
            st.warning("No tiers: No connection to the database or your databse is corrupt")
            st.stop()
        # Field inputs
        with st.form("uadd_form", border=False, enter_to_submit=False):
            st.text_input(
                "Name",
                max_chars=50,
                key="add_cable_name"
            )
            st.selectbox(
                "Select Tier",
                tiers,
                key="add_cable_tier_name"
            )
            st.number_input(
                "Density",
                min_value=1,
                max_value=65536,
                step=1,
                format="%d",
                key="add_cable_density"
            )
            st.number_input(
                "Max Amp",
                min_value=1,
                max_value=65536,
                step=1,
                format="%d",
                key="add_cable_max_amp"
            )
            st.number_input(
                "Power Loss",
                min_value=0,
                max_value=65536,
                step=1,
                format="%d",
                key="add_cable_loss"
            )
            st.form_submit_button("Add", on_click=addCable)