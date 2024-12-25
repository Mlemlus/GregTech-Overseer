import streamlit as st
from streamlit import session_state as ss
import requests
import pandas as pd
from datetime import datetime

#### Session state inicializations ####
if "update_pn_clicked_old_name" not in ss: # for each pn holds the state of update process
    ss.update_pn_clicked_old_name = ""

if "delete_pn_clicked_name" not in ss:
    ss.delete_pn_clicked_name = ""


#### Functions ####
def addPN():
    try:
        if len(ss["add_pn_name"]) >= 1:
            # post new pn info to API
            response = requests.post(
                "http://10.21.31.5:40649/api/add/power-network", 
                json={
                    "name": ss["add_pn_name"],
                    "cable_name": ss["add_pn_cable_name"],
                    "username": ss["username"]
                    })
            data = response.json()
            if data['status']: # returned status
                ss.backlog_message = "Power Network added"
            else:
                ss.backlog_message ="Failed to add power network"
        else:
            ss.backlog_message="Power Network name too short"
    except Exception as e:
        ss.backlog_message = f"addPN error: {e}"


def updatePN():
    # min length checks
    if len(ss["update_pn_clicked_name"]) <= 1:
        ss.backlog_message = "Power Network name too short"
    else:
        # post update pn info to API
        response = requests.post(
            "http://10.21.31.5:40649/api/update/power-network",
            json={
                "old_name":ss["update_pn_clicked_old_name"],
                "name":ss["update_pn_clicked_name"],
                "cable_name":ss["update_pn_clicked_cable_name"]
                })
        data = response.json()
        ss["update_pn_clicked_old_name"] = "" # reset edit state
        if data['status']:
            ss.backlog_message = "Power Network updated"
        else:
            ss.backlog_message ="Failed to update power network"

def deletePN():
    # post delete pn info to API
    response = requests.post("http://10.21.31.5:40649/api/delete/power-network", json={"name":ss["delete_pn_clicked_name"]})
    data = response.json()
    ss["delete_pn_clicked_name"] = "" # reset delete state
    if data['status']:
        ss.backlog_message = "Power Network deleted"
    else:
        ss.backlog_message ="Failed to delete power network"


#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.info(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Power Network Managment")

## select pns form ##
st.write("### List of power networks")
response = requests.get("http://10.21.31.5:40649/api/get/power-networks")
if not response.json()["status"]:
    st.error("No Power Networks :(")
    df = pd.DataFrame([['']*4], columns=["Name","Cable","Created at", "Owner"])
else:
    df = pd.DataFrame(response.json()["pns"], columns=["Name","Cable","Created at", "Owner"])

# List of pns container
with st.container(height=300):
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.write("Name")
    col2.write("Cable")
    col3.write("Created at")
    col4.write("Owner")
    for _ , row in df.iterrows(): # iterate throught entries
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.write(row["Name"])
        col2.write(row["Cable"])
        if not row["Created at"] == '':
            col3.write(datetime.strptime(row["Created at"], "%a, %d %b %Y %H:%M:%S %Z").strftime("%d %b %Y")) # just the date
        col4.write(row["Owner"])

        if not row["Name"] == '': # display buttons if we got any pns
            # Edit button logic
            if col5.button(label="Edit", key=f"edit_{row["Name"]}"): # needs unique key
                ss["update_pn_clicked_old_name"] = row["Name"] # sets the name to be edited in dataframe
                ss["delete_pn_clicked_name"] = "" # resets delete state
                st.rerun()

            # Edit row logic
            if ss["update_pn_clicked_old_name"] == row["Name"]:
                # get cables list
                response = requests.get("http://10.21.31.5:40649/api/get/cable-names")
                if response.json()["status"]:
                    cables = [i[0] for i in response.json()["cables"]]
                else:
                    st.warning("No cables: First add some cables in the Utils/Cables tab")
                    st.stop()

                # update form
                with st.form("update_form", border=False, enter_to_submit=False):
                    st.text_input(
                        "Name",
                        max_chars=50,
                        value=row["Name"],
                        key="update_pn_clicked_name"
                    )
                    st.selectbox(
                        "Select Cable",
                        cables,
                        index=cables.index(row["Cable"]),
                        key="update_pn_clicked_cable_name"
                    )
                    st.form_submit_button("Confirm changes", on_click=updatePN)

            # Delete button logic
            if col6.button(label="Delete", key=f"delete_{row["Name"]}"): # needs unique key
                ss["delete_pn_clicked_name"] = row["Name"] # sets the name to be delete in dataframe
                ss["update_pn_clicked_old_name"] = "" # Resets edit state
                st.rerun()
            
            # Delete row logic
            if ss["delete_pn_clicked_name"] == row["Name"]:
                if st.button(f"Confirm deletion of {row['Name']}"):
                    deletePN()
                    st.rerun()



## Add pn form ##
st.write("### Add Power Network")
# get cables list
response = requests.get("http://10.21.31.5:40649/api/get/cable-names")
if response.json()["status"]:
    cables = [i[0] for i in response.json()["cables"]]
else:
    st.warning("No cables: First add some cables in the Utils/Cables tab")
    st.stop()
# Field inputs
with st.form("uadd_form", border=False, enter_to_submit=False):
    st.text_input(
        "Name",
        max_chars=50,
        key="add_pn_name"
    )
    st.selectbox(
        "Select Cable",
        cables,
        key="add_pn_cable_name"
    )
    st.form_submit_button("Add", on_click=addPN)