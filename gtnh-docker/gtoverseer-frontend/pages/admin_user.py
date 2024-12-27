import streamlit as st
from streamlit import session_state as ss
import requests
import pandas as pd

#### Session state inicializations ####
if "add_user_condition" not in ss: # Condition checks for input requirements
    ss.add_user_condition = [False,False,False]

if "update_user_clicked_old_username" not in ss: # holds the selected username of update process
    ss.update_user_clicked_old_username = ""

if "delete_user_clicked_username" not in ss:
    ss.delete_user_clicked_username = ""


#### Functions ####
def addUser():
    try:
        # post new user info to API
        response = requests.post(
            "http://10.21.31.5:40649/api/add/user",
            json={
                "username":ss.add_user_username,
                "email": ss.add_user_email,
                "password": ss.add_user_password,
                "privileges":privilegeTable("add")
                })
        data = response.json()
        if data['status']: # status is a boolean
            ss.backlog_message = "User added"
        else:
            ss.backlog_message = f"Failed to add user:{data["error"]}"
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
        response = requests.post(
            "http://10.21.31.5:40649/api/update/user", 
            json={
                "old_username":ss["update_user_clicked_old_username"], 
                "username":ss["update_user_clicked_username"], 
                "email":ss["update_user_clicked_email"],
                "privileges":privilegeTable("update")
                })
        data = response.json()
        ss["update_user_clicked_old_username"] = "" # reset edit state
        if data['status']:
            ss.backlog_message = "User updated"
        else:
            ss.backlog_message = f"Failed to update user: {data["error"]}"

def deleteUser():
    # post delete user info to API
    response = requests.post("http://10.21.31.5:40649/api/delete/user", json={"username":ss["delete_user_clicked_username"]})
    data = response.json()
    ss["delete_user_clicked_username"] = "" # reset delete state
    if data['status']:
        ss.backlog_message = "User deleted!"
    else:
        ss.backlog_message ="Failed to delete user"

def privilegeTable(operation:str): # returns a table of privileges based on the operation (add/edit)
    output = []
    operation = operation + "_"
    # It is what it is (should have used st.pills)
    # Also added privileges that cannot be selected so I dont have to write this in future
    if ss[operation+"machine_add"]: output.append("Add Machines")
    if ss[operation+"machine_edit"]: output.append("Edit Machines")
    if ss[operation+"machine_remove"]: output.append("Remove Machines")
    if ss[operation+"ps_add"]: output.append("Add Power Source Machines")
    if ss[operation+"ps_edit"]: output.append("Edit Power Source Machines")
    if ss[operation+"ps_remove"]: output.append("Remove Power Source Machines")
    if ss[operation+"pn_add"]: output.append("Add Power Networks")
    if ss[operation+"pn_edit"]: output.append("Edit Power Networks")
    if ss[operation+"pn_remove"]: output.append("Remove Power Networks")
    if ss[operation+"cable_add"]: output.append("Add Cables")
    if ss[operation+"cable_edit"]: output.append("Edit Cables")
    if ss[operation+"cable_remove"]: output.append("Remove Cables")
    if ss[operation+"view_logs"]: output.append("View Logs")
    if ss[operation+"manage_maintenance"]: output.append("Manage Maintenance")
    if ss[operation+"administrator"]: output.append("Administrator")
    return output


#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.toast(ss.backlog_message)
    if ss.backlog_message == "User deleted!":
        st.balloons()
    ss.backlog_message = ""

## Header ##
st.write("# Admin User Managment")

## select users form ##
st.write("### List of users")
response = requests.get("http://10.21.31.5:40649/api/get/users")
df = pd.DataFrame(response.json()["users"], columns=["username", "email"])

# List of users container
with st.container(height=500):
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    col1.write("Username")
    col2.write("Email")
    for _ , row in df.iterrows(): # iterate throught entries
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1]) # columns for values and buttons
        col1.write(row["username"])
        col2.write(row["email"])

        # Edit button logic
        if row["username"] != ss.username:
            if col3.button(label="Edit", key=f"edit_{row["username"]}"): # needs unique key
                ss["update_user_clicked_old_username"] = row["username"] # sets the username to be edited in dataframe
                ss["delete_user_clicked_username"] = "" # resets delete state
                st.rerun()
            # Edit row logic 
            if ss["update_user_clicked_old_username"] == row["username"]:
                    # get user privileges
                    priv = requests.post("http://10.21.31.5:40649/api/get/user",json={"username":row["username"]}).json()["privileges"]
                    # Update form
                    with st.form("update_form", border=False, enter_to_submit=False):
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
                        c1, c2, c3, c4, c5 = st.columns(5)
                        # This would be much easier with multiselect or pills but it woudn't look as good
                        c1.write("Machines")
                        c1.checkbox("Add", key="update_machine_add", value=True if "Add Machines" in priv else False, disabled=True)
                        c1.checkbox("Edit", key="update_machine_edit", value=True if "Edit Machines" in priv else False, disabled=False)
                        c1.checkbox("Remove", key="update_machine_remove", value=True if "Remove Machines" in priv else False, disabled=False)
                        c2.write("Power Source Machines")
                        c2.checkbox("Add", key="update_ps_add", value=True if "Add Power Source Machines" in priv else False, disabled=True)
                        c2.checkbox("Edit", key="update_ps_edit", value=True if "Edit Power Source Machines" in priv else False, disabled=False)
                        c2.checkbox("Remove", key="update_ps_remove", value=True if "Remove Power Source Machines" in priv else False, disabled=True)
                        c3.write("Power Networks")
                        c3.checkbox("Add", key="update_pn_add", value=True if "Add Power Networks" in priv else False, disabled=False)
                        c3.checkbox("Edit", key="update_pn_edit", value=True if "Edit Power Networks" in priv else False, disabled=False)
                        c3.checkbox("Remove", key="update_pn_remove", value=True if "Remove Power Networks" in priv else False, disabled=False)
                        c4.write("Cables")
                        c4.checkbox("Add", key="update_cable_add", value=True if "Add Cables" in priv else False, disabled=False)
                        c4.checkbox("Edit", key="update_cable_edit", value=True if "Edit Cables" in priv else False, disabled=False)
                        c4.checkbox("Remove", key="update_cable_remove", value=True if "Remove Cables" in priv else False, disabled=False)
                        c5.write("Other")
                        c5.checkbox("View Logs", key="update_view_logs", value=True if "View Logs" in priv else False, disabled=False)
                        c5.checkbox("Manage Maintenance", key="update_manage_maintenance", value=True if "Manage Maintenance" in priv else False, disabled=False)
                        c5.checkbox("Administrator", key="update_administrator", value=True if "Administrator" in priv else False, disabled=False)
                        # oh god what have I done
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
c1, c2, c3, c4, c5 = st.columns(5)
# This would be much easier with multiselect or pills but it woudn't look as good
c1.write("Machines")
c1.checkbox("Add", key="add_machine_add", value=False, disabled=True)
c1.checkbox("Edit", key="add_machine_edit", value=False, disabled=False)
c1.checkbox("Remove", key="add_machine_remove", value=False, disabled=False)
c2.write("Power Source Machines")
c2.checkbox("Add", key="add_ps_add", value=False, disabled=True)
c2.checkbox("Edit", key="add_ps_edit", value=False, disabled=False)
c2.checkbox("Remove", key="add_ps_remove", value=False, disabled=True)
c3.write("Power Networks")
c3.checkbox("Add", key="add_pn_add", value=False, disabled=False)
c3.checkbox("Edit", key="add_pn_edit", value=False, disabled=False)
c3.checkbox("Remove", key="add_pn_remove", value=False, disabled=False)
c4.write("Cables")
c4.checkbox("Add", key="add_cable_add", value=False, disabled=False)
c4.checkbox("Edit", key="add_cable_edit", value=False, disabled=False)
c4.checkbox("Remove", key="add_cable_remove", value=False, disabled=False)
c5.write("Other")
c5.checkbox("View Logs", key="add_view_logs", value=False, disabled=False)
c5.checkbox("Manage Maintenance", key="add_manage_maintenance", value=False, disabled=False)
c5.checkbox("Administrator", key="add_administrator", value=False, disabled=False)

if st.button("Add", disabled=not all(ss.add_user_condition)):
    addUser()
    st.rerun()
