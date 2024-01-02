import streamlit as st
import json
import os
import bcrypt

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
                return json.load(file)
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

    # Process the form when the user clicks 'Register'
    submit_button = st.form_submit_button("Register")

if submit_button:
    # Check if passwords match
    if password != confirm_password:
        st.error("Passwords do not match. Please re-enter matching passwords.")
    else:
        # Save user data
        hashed_password = hash_password(password)
        users.append({"name": name, "age": age, "sex": sex, "dob": str(dob), 
                      "email": email, "password": hashed_password,
                      "image": user_image.getvalue() if user_image is not None else None})
        handle_json(file_name, users, write=True)
        st.success("Registered successfully!")

# Consider adding features to view and edit user profiles
if st.button('Download My Data'):
    # Assuming you have a way to identify the current user, e.g., through their email
    current_user_email = "example@email.com"  # Replace with actual method to get current user's email
    current_user_data = next((user for user in users if user["email"] == current_user_email), None)
    if current_user_data:
        json_str = json.dumps(current_user_data, indent=4)
        st.download_button(label="Download My Data", data=json_str, file_name="my_data.json", mime="text/json")
    else:
        st.error("User data not found.")

# Add a button to download all user data as JSON
if st.button('Download All User Data'):
    json_str_all = json.dumps(users, indent=4)
    st.download_button(label="Download All User Data", data=json_str_all, file_name="all_user_data.json", mime="text/json")