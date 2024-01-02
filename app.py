import streamlit as st
import json
import os
import bcrypt

# Ensure bcrypt is installed: pip install bcrypt

# Function to securely hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to check if a hashed password matches a user's password
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# Function to handle JSON data
def handle_json(file_name, data=None, write=False):
    if write:
        with open(file_name, "w") as file:
            json.dump(data, file)
    else:
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []  # Return empty list if JSON is invalid
        return []

# Main Streamlit application
st.title("Mams")

# Load existing user data
file_name = "user_data.json"
users = handle_json(file_name)

# Input form for new user
with st.form("User Registration"):
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=0, max_value=120, value=0)
    sex = st.radio("Select Your Sex", ["Male", "Female"])
    job_field = st.selectbox("What is your Job field", 
                             ('Academic', 'IT', 'Real Estate Business', 
                              'Local Business', 'Salesman', 'Manager', 'Medical'))
    dob = st.date_input("When's your birthday")
    email = st.text_input("Enter your E-Mail address")
    password = st.text_input("Create your password", type="password")
    confirm_password = st.text_input("Re-enter your password", type="password")
    user_image = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

    submit_button = st.form_submit_button("Register")

if submit_button:
    if password != confirm_password:
        st.error("Passwords do not match. Please re-enter matching passwords.")
    else:
        hashed_password = hash_password(password)
        user_data = {"name": name, "age": age, "sex": sex, "dob": str(dob), 
                     "email": email, "password": hashed_password}
        if user_image is not None:
            # Read image as bytes
            user_data["image"] = user_image.getvalue()
        users.append(user_data)
        handle_json(file_name, users, write=True)
        st.success("Registered successfully!")

# Download My Data Button
if st.button('Download My Data'):
    # Replace this with the actual method to get the current user's email
    current_user_email = "example@email.com"
    current_user_data = next((user for user in users if user["email"] == current_user_email), None)
    if current_user_data:
        json_str = json.dumps(current_user_data, indent=4)
        st.download_button(label="Download My Data", data=json_str, file_name="my_data.json", mime="text/json")
    else:
        st.error("User data not found.")

# Download All User Data Button
if st.button('Download All User Data'):
    json_str_all = json.dumps(users, indent=4)
    st.download_button(label="Download All User Data", data=json_str_all, file_name="all_user_data.json", mime="text/json")
