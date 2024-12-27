import streamlit as st
from streamlit import session_state as ss
import requests
import pandas as pd


#response = requests.get('http://10.21.31.5:40649/data')
#data = response.json()

#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.toast(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Dashboard")


## Table ##
st.write("### Machine status")
# df = pd.DataFrame(data, columns=[ "ID", "Name", "OC Address", "Amp", "Created at", "x", "y", "z", "Chunk Loaded", "Work Progress %", "Operational", "Power Network"])
# df["coords (x,y,z)"] = df["x"].astype(str) + "," + df["y"].astype(str) +  "," + df["z"].astype(str)
# df = df.drop(columns=["x", "y", "z"])
# st.dataframe(df)
