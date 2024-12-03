import streamlit as st
if st.button("Log in"):
    st.session_state.logged_in = True
    st.rerun()