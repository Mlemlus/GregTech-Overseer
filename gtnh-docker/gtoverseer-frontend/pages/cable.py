import streamlit as st
from streamlit import session_state as ss
# add/edit/remove cables


#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.info(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Cables")