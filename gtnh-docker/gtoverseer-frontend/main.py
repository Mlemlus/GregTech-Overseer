import requests
import streamlit as st
import pandas as pd

response = requests.get('http://10.21.31.5:40649/data')  
data = response.json()
st.write(data)
df = pd.DataFrame(data)
st.dataframe(df)  
