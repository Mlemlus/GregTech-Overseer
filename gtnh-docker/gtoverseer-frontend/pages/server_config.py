import streamlit as st, requests
from streamlit import session_state as ss

#### Functions ####
def updateConfig():
    response = requests.post(
        "http://10.21.31.5:40649/api/update/server-config",
        json={
            "oc_stations_update_rate":ss["server_config_1"],
            "oc_stations_reinitialization_rate":ss["server_config_2"],
            })
    data = response.json()
    if data['status']:
        ss.backlog_message = "Server Configuration Updated"


#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.info(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Server settings")

## Configuration options ##
response = requests.get("http://10.21.31.5:40649/api/get/server-config")
if not response.json()["status"]:
    st.error("No backend connection, what did you do to get here?")
    st.stop()
response = response.json()
with st.form("server config form", border=False):
    st.write("#### OC sleep between updates in ms")
    st.caption("Too low values may cause lag!")
    st.slider(
        label="oc update rate",
        label_visibility="hidden",
        key="server_config_1",
        min_value=100,
        max_value=5000,
        value=int(response["oc_stations_update_rate"]))

    st.write("#### Time between GT machine to controller reconection in minutes")
    st.caption("Time how often OC checks for a newly connected machine")
    st.slider(
        label="oc reinitialization rate",
        label_visibility="hidden",
        key="server_config_2",
        min_value=1,
        max_value=60,
        value=int(response["oc_stations_reinitialization_rate"]))

    if st.form_submit_button("Confirm changes"):
        updateConfig()
        st.rerun()