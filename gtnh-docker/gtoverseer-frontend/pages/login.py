import streamlit as st
import requests

#### Functions ####
def login(email, password):
    try:
        # check with backend if login info is correct, if yes recieve username
        response = requests.post("http://10.21.31.5:40649/api/authenticate", json={"email": str(email), "password": str(password)})
        data = response.json()
        if data["status"]: # status is a boolean
            st.session_state.username = data["username"] # set session username
            st.session_state.logged_in = True
            st.session_state.backlog_message = "Login successful"
        else:
            st.session_state.backlog_message ="Authentication failed"
    except Exception as e:
        st.error(f"Error connecting to authentication server: {e}")

#### Body ####
st.write("# Login")
st.write("> Please log in to continue")

# login form
with st.form("login_form"):
    email = st.text_input("Email", max_chars=50)
    password = st.text_input("Password", type="password", max_chars=100)
    submit = st.form_submit_button("Login")
    if submit:
        login(email, password)
        st.rerun()