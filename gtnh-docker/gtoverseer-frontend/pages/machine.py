import streamlit as st
from streamlit import session_state as ss
# machine config/info



#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.info(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Machines")