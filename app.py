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
    page = st.sidebar.selectbox("Choose your page", ["Register", "Login","Developer Options"])

    if page == "Register":
        register_page()
    elif page == "Login":
        login_page()
    elif page== "Developer Options":
        developer_page()

def register_page():

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
            expenses1.append({"name":name,"age": age , "sex":sex, "dob": str(dob), "image": user_image})
            expenses2.append({"email":email,"password":password})
            save_details(file_name1, expenses1)
            save_details(file_name2, expenses2)

            st.write("Sucessfuly Registered")

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

def developer_page():
    st.header("Login As Admin")

    # Initialize session states
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    email = st.text_input("Email of admin")
    password = st.text_input("Password of admin", type="password")

    if st.button("Login"):
        if email == "Rockarush2@gmail.com" and password == "Arush@2003":
            st.success("Login successful!")
            st.session_state.logged_in = True
        else:
            st.error("Invalid email or password")
            st.session_state.logged_in = False

    if st.session_state.logged_in:
        # Button for downloading JSON file
        with open("user_data.json", "r") as file:
            st.download_button(label="Download JSON", data=file, file_name="user_data.json", mime="application/json")

# Run the main application
if __name__ == "__main__":
    main()