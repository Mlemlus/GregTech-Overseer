import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")


dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)
pw_network_page = st.Page("pages/power_network.py", title="Power Networks", icon=":material/bolt:")
machine_page = st.Page("pages/machine.py", title="Machines", icon=":material/factory:")


user_config = st.Page("pages/user_config.py", title="Profile settings", icon=":material/settings:")
server_config = st.Page("pages/server_config.py", title="Server configuration", icon=":material/settings:")

# bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
# alerts = st.Page(
#    "reports/alerts.py", title="System alerts", icon=":material/notification_important:"
# )

# search = st.Page("tools/search.py", title="Search", icon=":material/search:")
# history = st.Page("tools/history.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Reports": [dashboard, machine_page, pw_network_page],
            "Tools": [server_config],
            "Account": [user_config, logout_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()