import streamlit as st
from streamlit import session_state as ss
import requests
import pandas as pd


#response = requests.get('http://10.21.31.5:40649/data')  
#data = response.json()
data = [[11,"basicmachine.distillery.tier.01","91f56438-5bc3-4bc7-a968-b9cdbd8eebd5",1,"Mon, 02 Dec 2024 22:08:01 GMT",32,130,25,False,0,True,0],[10,"multimachine.multifurnace","5c4e452a-f6e3-4ecf-9699-4861969d7ee8",1,"Mon, 02 Dec 2024 22:08:01 GMT",13,130,25,False,0,True,0],[2,"multimachine.blastfurnace","0c6a57c0-b270-4bc4-91c0-b9e47b6c0b64",2,"Mon, 02 Dec 2024 22:08:01 GMT",23,130,22,False,0,True,0],[5,"multimachine.blastfurnace","5b4e5b09-e230-4a07-a8b5-af765c560ccc",2,"Mon, 02 Dec 2024 22:08:01 GMT",28,130,25,False,0,True,0],[8,"basicgenerator.diesel.tier.03","ec119845-80cd-474a-9b32-9339a9ea61f7",1,"Mon, 02 Dec 2024 22:08:01 GMT",13,129,26,False,0,True,0],[6,"basicgenerator.diesel.tier.03","6d0d95b2-fe48-412c-9613-435083dfea9d",1,"Mon, 02 Dec 2024 22:08:01 GMT",28,129,26,False,0,True,0],[4,"basicgenerator.diesel.tier.03","5edfda01-1a89-4e35-8e3c-595b5dd9a526",1,"Mon, 02 Dec 2024 22:08:01 GMT",18,129,26,False,0,True,0],[1,"basicgenerator.diesel.tier.03","15f3add0-ee29-4b9c-b453-12177d962ec9",1,"Mon, 02 Dec 2024 22:08:01 GMT",23,129,21,False,0,True,0],[3,"multimachine.blastfurnace","b98f5ba5-c50e-47f8-96c1-eb0ce9dba5ca",2,"Mon, 02 Dec 2024 22:08:01 GMT",18,130,25,False,0,True,0],[9,"multimachine.blastfurnace","4876e40e-22f5-4e21-b605-6682f4f23f7a",2,"Mon, 02 Dec 2024 22:08:01 GMT",23,130,25,False,0,True,0],[7,"basicgenerator.diesel.tier.03","fabac348-4224-4ead-b703-ffcd7882b940",1,"Mon, 02 Dec 2024 22:08:01 GMT",30,130,27,False,0,True,0]]

#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.info(ss.backlog_message)
    ss.backlog_message = ""

## Haader ##
st.write("# Dashboard")


## Table ##
st.write("### Machine status")
df = pd.DataFrame(data, columns=[ "ID", "Name", "OC Address", "Amp", "Created at", "x", "y", "z", "Chunk Loaded", "Work Progress %", "Operational", "Power Network"])
df["coords (x,y,z)"] = df["x"].astype(str) + "," + df["y"].astype(str) +  "," + df["z"].astype(str)
df = df.drop(columns=["x", "y", "z"])
st.dataframe(df)
