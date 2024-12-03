import streamlit as st
import requests, time
from PIL import Image
from io import BytesIO

if "logged_in" not in st.session_state: # init login status tracking
    st.session_state.logged_in = False

if "show_logout_confirm" not in st.session_state: # init logout process tracking
    st.session_state.show_logout_confirm = False


username = "meemlus" ###################

@st.cache_data
def fetch_image(username): # get profile picture, uses mineatar.io and mojang public API
    try:
        response_uuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}?')
        response_uuid.raise_for_status() # throw error if problem
        uuid = response_uuid.json()['id']
        response_image = requests.get(f"https://api.mineatar.io/face/{uuid}")
        response_image.raise_for_status()  
        return Image.open(BytesIO(response_image.content))
    except Exception:
        return False # probably should implement troll face instead


login_page = st.Page("pages/login.py", title="Log in", icon=":material/login:")
#logout_page = st.Page(logout, title="Log out", icon=":material/logout:")


dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)

pw_network_page = st.Page("pages/power_network.py", title="Power Networks", icon=":material/bolt:")
machine_page = st.Page("pages/machine.py", title="Machines", icon=":material/factory:")
server_config = st.Page("pages/server_config.py", title="Server configuration", icon=":material/settings:")
cable_page = st.Page("pages/cable.py", title="Cables", icon=":material/cable:")

user_config = st.Page("pages/user_config.py", title="Profile settings", icon=":material/settings:")

# bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
# alerts = st.Page(
#    "reports/alerts.py", title="System alerts", icon=":material/notification_important:"
# )

# search = st.Page("tools/search.py", title="Search", icon=":material/search:")
# history = st.Page("tools/history.py", title="History", icon=":material/history:")

##### Sidebar logged in stuff
if st.session_state.logged_in and st.session_state.show_logout_confirm == False:
    col1, col2 = st.sidebar.columns([1,2])
    col1.write("Logged in as:")
    if fetch_image(username):
        col2.image(fetch_image(username), caption="meemlus")
    else:
        col2.text(username)
    if col1.button("Logout"):
        st.session_state.show_logout_confirm = True
        st.rerun()

if st.session_state.show_logout_confirm:
    st.sidebar.warning("Are you sure you want to logout?")
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Yes"):
        st.session_state.logged_in = False
        st.session_state.show_logout_confirm = False
        st.rerun()
    if col2.button("Cancel"):
        st.session_state.show_logout_confirm = False
        st.rerun()



if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Reports": [dashboard,],
            "Utils": [machine_page, pw_network_page, cable_page, server_config],
            "Account": [user_config],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()