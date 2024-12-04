import streamlit as st
import requests

#### Functions ####
def addUser(username, email, password):
    try:
        # check with backend if login info is correct, if yes recieve username
        response = requests.post("http://10.21.31.5:40649/api/add/user", json={"username":username, "email": email, "password": password})
        if response['status']: # status is a boolean
            st.session_state.backlog_message = "User added"
        else:
            st.session_state.backlog_message ="Failed to add user"

    except Exception as e:
        st.error(f"Error connecting to authentication server: {e}")


#### Body ####
st.write("# Admin User Managment")

st.write("### Add a user")
# add user form
with st.form("add_user_form"):
    username = st.text_input("Username", max_chars=16)
    email = st.text_input("Email", max_chars=50)
    password = st.text_input("Password", type="password", max_chars=100)
    submit = st.form_submit_button("Add")
    if submit:
        addUser(username, email, password)
        st.rerun()