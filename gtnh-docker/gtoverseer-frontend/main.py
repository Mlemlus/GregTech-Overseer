import streamlit as st
from streamlit import session_state as ss
import requests, os
from PIL import Image
from io import BytesIO

## Page config ##
st.set_page_config(page_title="GregTech Overseer", layout="wide")

#### Session state inicializations ####
if "show_logout_confirm" not in ss: # init logout process tracking
    ss.show_logout_confirm = False

if "backlog_message" not in ss: # init message that passes through page reload
    ss.backlog_message = ""

if "username" not in ss: # init login status tracking
    ss.username = ""

if "privileges" not in ss:
    ss.privileges = []

#### Functions ####
@st.cache_data
def fetch_image(username): # get profile picture, uses mineatar.io and mojang public API
    try:
        response_uuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}?')
        response_uuid.raise_for_status() # throws HTTPError if response is error
        uuid = response_uuid.json()['id']
        response_image = requests.get(f"https://api.mineatar.io/face/{uuid}")
        response_image.raise_for_status()
        return Image.open(BytesIO(response_image.content))
    except Exception:
        return False # probably should implement troll face instead


#### Pages ####
## Login/Authentication ##
login_page = st.Page("pages/login.py", title="Log in", icon=":material/login:")

## Reports ##
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)

## Utils ##
pw_network_page = st.Page("pages/power_network.py", title="Power Networks", icon=":material/bolt:")
machine_page = st.Page("pages/machine.py", title="Machines", icon=":material/factory:")
cable_page = st.Page("pages/cable.py", title="Cables", icon=":material/cable:")
power_source_page = st.Page("pages/power_source.py", title="Power Source Machines", icon=":material/power:")

## Configuration ##
user_config = st.Page("pages/user_config.py", title="Profile settings", icon=":material/account_circle:")
server_config = st.Page("pages/server_config.py", title="Server configuration", icon=":material/settings:")

## Admin only pages ##
admin_manage_user = st.Page("pages/admin_user.py", title="Users managment", icon=":material/group:")

#### Body ####
## Sidebar navigation ##
if ss.username != "":
    navigation = {
            "Reports": [dashboard],
            "Utils": [machine_page,power_source_page , pw_network_page, cable_page],
            "Configuration": [user_config]
            }
    if "Administrator" in ss.privileges:
        navigation["Administration"] = [admin_manage_user]
    if "Server Configuration" in ss.privileges or "Administrator" in ss.privileges:
        navigation["Configuration"].append(server_config)
    pg = st.navigation(navigation)
else:
    pg = st.navigation([login_page])

## Sidebar logged in stuff ##
# Default logged in state
if ss.username != "" and ss.show_logout_confirm == False:
    col1, col2 = st.sidebar.columns([1,2])
    col1.write("Logged in as:")
    if fetch_image(ss.username):
        col2.image(fetch_image(ss.username), caption=ss.username)
    else:
        col2.text(ss.username)
    if col1.button("Logout"):
        ss.show_logout_confirm = True
        st.rerun()

# Logging out state
if ss.show_logout_confirm:
    st.sidebar.warning("Are you sure you want to logout?")
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Yes"):
        ss.show_logout_confirm = False
        ss.username = ""
        ss.backlog_message = "Successfully logged out"
        st.rerun()
    if col2.button("Cancel"):
        ss.show_logout_confirm = False
        st.rerun()


#### "Main" ####
pg.run()