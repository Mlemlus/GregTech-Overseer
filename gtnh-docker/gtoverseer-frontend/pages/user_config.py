import streamlit as st
from streamlit import session_state as ss
import requests


#### Functions ####
def changePassword(new_password):
    response = requests.post(
        "http://10.21.31.5:40649/api/update/user-password",
        json={
            "username": ss.username,
            "new_password": new_password
        })
    data = response.json()
    if data["status"]:
        ss.backlog_message = "Password updated."
        requests.post("http://10.21.31.5:40649/log",json={
            "text":f"{ss["username"]} updated password",
            "username":ss.username
        })
    else:
        ss.backlog_message = f"Failed to change password:{data["error"]}"


#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.toast(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# User Settings")

# Streamlit UI for change password
st.write("### Change Password")

# Create a form for password change
with st.form("change_password_form"):
    new_password = st.text_input("New Password", type="password", placeholder="Enter your new password")
    confirm_password = st.text_input("Confirm New Password", type="password", placeholder="Confirm your new password")

    if st.form_submit_button("Change Password"):
        if not new_password or not confirm_password:
            st.warning("Please fill out all fields")
        elif new_password != confirm_password:
            st.warning("New password does not match")
        elif len(new_password) < 8:
            st.warning("New password must be at least 8 characters long")
        else:
            changePassword(new_password)
            st.rerun()