import streamlit as st
from streamlit import session_state as ss
import requests
import pandas as pd

#### Session state inicializations ####
if "add_user_condition" not in ss:
    ss.add_user_condition = [False,False,False]

if "update_user_clicked_old_username" not in ss: # for each users holds the state of update process
    ss.update_user_clicked_old_username = ""

if "delete_user_clicked_username" not in ss:
    ss.delete_user_clicked_username = ""


#### Functions ####
def addUser(username, email, password):
    try:
        # post new user info to API
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

def updateUser():
    # min length checks
    if len(ss["update_user_clicked_username"]) <= 3:
        ss.backlog_message = "Username too short"
    elif len(ss["update_user_clicked_email"]) <= 5:
        ss.backlog_message = "Email too short"
    else:
        # post update user info to API
        response = requests.post("http://10.21.31.5:40649/api/update/user", json={"old_username":ss["update_user_clicked_old_username"], "username":ss["update_user_clicked_username"], "email":ss["update_user_clicked_email"]})
        data = response.json()
        ss["update_user_clicked_old_username"] = "" # reset edit state
        if data['status']:
            ss.backlog_message = "User updated"
        else:
            ss.backlog_message ="Failed to update user"

def deleteUser():
    # post delete user info to API
    response = requests.post("http://10.21.31.5:40649/api/delete/user", json={"username":ss["delete_user_clicked_username"]})
    data = response.json()
    ss["delete_user_clicked_username"] = "" # reset delete state
    if data['status']:
        ss.backlog_message = "User deleted"
    else:
        ss.backlog_message ="Failed to delete user"



#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.info(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Admin User Managment")

## select users form ##
st.write("### List of users")
response = requests.get("http://10.21.31.5:40649/api/get/users")
df = pd.DataFrame(response.json()["users"], columns=["username", "email"])

# List of users container
with st.container(height=300):
    for _ , row in df.iterrows(): # iterate throught entries
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1]) # columns for values and buttons
        col1.write(row["username"])
        col2.write(row["email"])

        # Edit button logic
        if col3.button(label="Edit", key=f"edit_{row["username"]}"): # needs unique key
            ss["update_user_clicked_old_username"] = row["username"] # sets the username to be edited in dataframe
            ss["delete_user_clicked_username"] = "" # resets delete state
            st.rerun()
        # Edit row logic 
        if ss["update_user_clicked_old_username"] == row["username"]:
                with st.form("update_form", border=False):
                    submit_username = st.text_input(
                        "Username",  
                        max_chars=16,
                        value=row["username"],
                        key="update_user_clicked_username" # holds value in session state beacuse buttons are stateless (smh)
                    )
                    submit_email = st.text_input(
                        "Email", 
                        max_chars=50,
                        value=row["email"],
                        key="update_user_clicked_email"
                    )
                    st.form_submit_button("Confirm changes", on_click=updateUser)

        # Delete button logic
        if col4.button(label="Delete", key=f"delete_{row["username"]}"): # needs unique key
            ss["delete_user_clicked_username"] = row["username"] # sets the username to be delete in dataframe
            ss["update_user_clicked_old_username"] = "" # Resets edit state
            st.rerun()
        # Delete row confirmation
        if ss["delete_user_clicked_username"] == row["username"]:
            if st.button(f"Confirm deletion of {row['username']}"):
                deleteUser()
                st.rerun()



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
