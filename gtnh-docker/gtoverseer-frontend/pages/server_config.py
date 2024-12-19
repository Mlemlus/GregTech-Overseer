import streamlit as st
from streamlit import session_state as ss
# server settings



#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.info(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Server settings")

## Configuration options ##
st.write("### OC sleep between updates in ms")
oc_update_rate = st.slider(label="oc update rate", label_visibility="hidden", min_value=0, max_value=5000, value=1000)
st.caption("Too low values may cause lag!")

st.write("### ")
