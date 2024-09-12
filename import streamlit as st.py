import streamlit as st
lab1 = st.Page("lab1.py",title="Lab 1")
lab2 = st.Page("lab2.py",title="Lab 2")
lab3 = st.Page("lab3.py",title="Lab 3", default=True)
pg = st.navigation([lab1, lab2, lab3])
st.set_page_config(page_title="Labs Manager")
pg.run()