import streamlit as st
from streamlit import session_state as ss






#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.toast(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# User Settings")

## profile settings ##
st.write("### Profile settings")