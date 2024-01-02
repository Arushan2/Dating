import streamlit as st
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", value=None)
sex = st.radio("Select Your Sex", ["Male", "Female"])
job_field = st.selectbox("What is your Job field", ('Academic', 'IT', 'Real Estate Business', 'Local Business', 'Salesman', 'Manager', 'Medical'))
dob = st.date_input("When's your birthday")