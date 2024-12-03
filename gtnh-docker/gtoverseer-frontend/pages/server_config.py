import streamlit as st
# server settings
st.write("# Server settings")

st.write("### OC sleep between updates")
oc_update_rate = st.slider(label="oc update rate", label_visibility="hidden", min_value=0, max_value=120)
st.caption("Too low values may cause lag!")

st.write("### ")
