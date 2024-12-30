import streamlit as st
from streamlit import session_state as ss
import requests

#### Functions ####
def login(email, password):
    try:
        # check with backend if login info is correct, if yes recieve username
        response = requests.post(
            "http://10.21.31.5:40649/api/authenticate",
            json={
                "email": str(email),
                "password": str(password)})
        data = response.json()
        if data["status"] and data["username"] != None: # status is a boolean
            ss.username = data["username"][0] # set session username
            ss.privileges = requests.post("http://10.21.31.5:40649/api/get/user",json={"username":data["username"][0]}).json()["privileges"]
            ss.logged_in = True
            ss.backlog_message = "Login successful"
            requests.post("http://10.21.31.5:40649/log",json={
                "text":f"{ss.username} successfully logged in",
                "username":ss.username
            })
        else:
            ss.backlog_message ="Email or password is not valid."
            requests.post("http://10.21.31.5:40649/log",json={
                "text":f"Failed login attempt with email: {email}"
            })
    except Exception as e:
        ss.backlog_message = f"Login error: {e}"
        requests.post("http://10.21.31.5:40649/log",json={
            "text":f"Frontend login error: {e}"
        })

#### Body ####
## Backlog info message print ###
if ss.backlog_message != "":
    st.toast(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Login")
st.write("> Please log in to continue")

## login form ####
with st.form("login_form"):
    email = st.text_input("Email", max_chars=50)
    password = st.text_input("Password", type="password", max_chars=100)
    submit = st.form_submit_button("Login")
    if submit:
        login(email, password)
        st.rerun()