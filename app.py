import streamlit as st
import json
import os
def Details_as_json(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.dumps(json.load(file))
    return json.dumps([])

# Function to load expenses from a JSON file
def load_details(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    return []

# Function to save expenses to a JSON file
def save_details(file_name, expenses):
    with open(file_name, "w") as file:
        json.dump(expenses, file)

# Main Streamlit application

st.title("Mams")

# Load existing expenses
file_name1 = "user_data.json"
file_name2="email_password_data.json"
personal_json = Details_as_json(file_name1)
password_json = Details_as_json(file_name2)
expenses1 = load_details(file_name1)
expenses2 = load_details(file_name2)


# Input form for new expenses
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", value=None)
sex = st.radio("Select Your Sex", ["Male", "Female"])
job_field = st.selectbox("What is your Job field", ('Academic', 'IT', 'Real Estate Business', 'Local Business', 'Salesman', 'Manager', 'Medical'))
dob = st.date_input("When's your birthday")

# Upload user image
user_image = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
email = st.text_input("Enter your E-Mail address")
password = st.text_input("Create your password", type="password")
confirm_password = st.text_input("Re-enter your password", type="password")

# Check if passwords match
passwords_match = password == confirm_password
if st.button("Register"):
    if not passwords_match:
        st.error("Passwords do not match. Please re-enter matching passwords.")
    else:
        expenses1.append({"name": name, "age": age, "sex": sex, "dob": str(dob), "image": user_image})
        expenses2.append({"email": email, "password": password})
        save_details(file_name1, expenses1)  # Save the updated details
        save_details(file_name2, expenses2)
        st.success("Successfully Registered")

# Download details as JSON button logic
if st.button("Download details as JSON"):
    # Load the file content as a string
    with open(file_name1, "r") as file:
        json_data = file.read()
    st.download_button(label="Download JSON", data=json_data, file_name="user_data.json", mime="application/json")
