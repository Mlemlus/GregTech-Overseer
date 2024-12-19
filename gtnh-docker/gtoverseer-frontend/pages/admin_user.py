import streamlit as st
from streamlit import session_state as ss
import requests

#### Session state inicializations ####
if "add_user_condition" not in ss:
    ss.add_user_condition = [False,False,False]



#### Functions ####
def addUser(username, email, password):
    try:
        # check with backend if login info is correct, if yes recieve username
        response = requests.post("http://10.21.31.5:40649/api/add/user", json={"username":username, "email": email, "password": password})
        data = response.json()
        if data['status']: # status is a boolean
            ss.backlog_message = "User added"
        else:
            ss.backlog_message ="Failed to add user"

    except Exception as e:
        ss.backlog_message = f"AddUser error: {e}"

def formReq(key, form, form_position, min_length): # damn im good
    ss[f"{form}_condition"][form_position] = len(ss[key]) >= min_length


#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.info(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Admin User Managment")

## Add user form ##
st.write("### Add user")
# Field inputs
# due to the fact that on_change fucntion is forbidden for text_input in forms, I will not be using forms
st.text_input(
    "Username",  
    max_chars=16,
    key="add_user_username",
    on_change=formReq,
    args=("add_user_username","add_user",0,3)
)
st.text_input(
    "Email", 
    max_chars=50,
    key="add_user_email",
    on_change=formReq,
    args=("add_user_email","add_user",1,5)
)
st.text_input(
    "Password", 
    type="password",
    max_chars=100,
    key="add_user_password",
    on_change=formReq,
    args=("add_user_password","add_user",2,8)
)

if st.button("Add", disabled=not all(ss.add_user_condition)):
    addUser(ss.add_user_username, ss.add_user_email, ss.add_user_password)
    st.rerun()
