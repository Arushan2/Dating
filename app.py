import streamlit as st
import json
import os

# Function to convert details to JSON
def details_as_json(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.dumps(json.load(file))
    return json.dumps([])

# Function to load details from a JSON file
def load_details(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    return []

# Function to save details to a JSON file
def save_details(file_name, details):
    with open(file_name, "w") as file:
        json.dump(details, file)

# Function to verify login credentials
def verify_login(email, password, file_name):
    users = load_details(file_name)
    for user in users:
        if user['email'] == email and user['password'] == password:
            return True
    return False

# Main Streamlit application
def main():
    st.title("Mams")

    # Page navigation
    page = st.sidebar.selectbox("Choose your page", ["Register", "Login"])

    if page == "Register":
        register_page()
    elif page == "Login":
        login_page()

# Register Page Function
def register_page():
    file_name1 = "user_data.json"
    file_name2 = "email_password_data.json"
    expenses1 = load_details(file_name1)
    expenses2 = load_details(file_name2)

    # Input form for new user
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", value=None)
    sex = st.radio("Select Your Sex", ["Male", "Female"])
    job_field = st.selectbox("What is your Job field", ('Academic', 'IT', 'Real Estate Business', 'Local Business', 'Salesman', 'Manager', 'Medical'))
    dob = st.date_input("When's your birthday")
    user_image = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
    email = st.text_input("Enter your E-Mail address")
    password = st.text_input("Create your password", type="password")
    confirm_password = st.text_input("Re-enter your password", type="password")

    # Check if passwords match and register user
    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match. Please re-enter matching passwords.")
        else:
            expenses1.append({"name": name, "age": age, "sex": sex, "dob": str(dob), "image": user_image})
            expenses2.append({"email": email, "password": password})
            save_details(file_name1, expenses1)
            save_details(file_name2, expenses2)
            st.success("Successfully Registered")

    # Button for downloading JSON file
    if st.button("Download User Details as JSON"):
        user_data = details_as_json(file_name1)
        st.download_button(label="Download JSON", data=user_data, file_name="user_data.json", mime="application/json")

# Login Page Function
def login_page():
    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_login(email, password, "email_password_data.json"):
            st.success("Login successful!")
            # Additional actions after successful login
        else:
            st.error("Invalid email or password")

# Run the main application
if __name__ == "__main__":
    main()
