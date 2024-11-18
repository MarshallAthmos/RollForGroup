import streamlit as st
from sidebar import sidebar

sidebar()

st.title("Home")
with open("frontend_res/homepage.md", "r", encoding="utf-8") as f:
    homepage_markdown = f.read()
st.markdown(homepage_markdown)
st.subheader("Let's Go! :fire:")