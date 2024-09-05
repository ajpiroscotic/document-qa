import streamlit as st

st.set_page_config(page_title="IST688_Labs", page_icon="✏️")


Lab_1 = st.Page("lab1.py", title="Lab 1")
Lab_2 = st.Page("lab2.py", title="Lab 2")


pages = [Lab_1, Lab_2]
page = st.navigation(pages)


page.run()
