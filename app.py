import streamlit as st
import json
import os
import hashlib

# Function to load details from a JSON file with error handling
def load_details(file_name):
    try:
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                return json.load(file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return []

# Function to save details to a JSON file with error handling
def save_details(file_name, details):
    try:
        with open(file_name, "w") as file:
            json.dump(details, file)
    except Exception as e:
        st.error(f"Error writing file: {e}")

# Hashing function for password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to verify login
def verify_login(email, password, file_name):
    users = load_details(file_name)
    hashed_password = hash_password(password)
    for user in users:
        if user['email'] == email and user['password'] == hashed_password:
            return True
    return False

# Function to find matches based on job field and age range
# Function to find matches based on job field and age range
def find_matches(user_data, age_range=5):
    matches = []
    for i, user in enumerate(user_data):
        if 'job_field' not in user or 'age' not in user or not isinstance(user['age'], int):
            continue  # Skip users without job_field or age or if age is not an integer
        for j, other_user in enumerate(user_data):
            if i != j and 'job_field' in other_user and 'age' in other_user and isinstance(other_user['age'], int):
                same_job_field = user['job_field'] == other_user['job_field']
                age_difference = abs(user['age'] - other_user['age'])
                if same_job_field and age_difference <= age_range:
                    matches.append((user, other_user))
    return matches


# Streamlit page layout for displaying matching details
def show_matching_page(user_data_file):
    user_data = load_details(user_data_file)
    matches = find_matches(user_data)
    st.title("Matching People's Details")
    for user, match in matches:
        st.subheader(f"{user['name']} matched with {match['name']}")
        st.text(f"Job Field: {user['job_field']}")
        st.text(f"Age: {user['age']} and {match['age']}")

def main():
    st.title("Mams")
    page = st.sidebar.selectbox("Choose your page", ["Register", "Login", "Developer Options"])
    if page == "Register":
        register_page()
    elif page == "Login":
        login_page()
    elif page == "Developer Options":
        developer_page()

def register_page():
    file_name1 = "user_data.json"
    file_name2 = "email_password_data.json"
    expenses1 = load_details(file_name1)
    expenses2 = load_details(file_name2)

    # Initialize session state for each input field
    if 'name' not in st.session_state:
        st.session_state['name'] = ''
    if 'age' not in st.session_state:
        st.session_state['age'] = 0
    if 'sex' not in st.session_state:
        st.session_state['sex'] = 'Male'
    if 'job_field' not in st.session_state:
        st.session_state['job_field'] = 'Academic'
    if 'dob' not in st.session_state:
        st.session_state['dob'] = None
    if 'user_image' not in st.session_state:
        st.session_state['user_image'] = None
    if 'email' not in st.session_state:
        st.session_state['email'] = ''
    if 'password' not in st.session_state:
        st.session_state['password'] = ''
    if 'confirm_password' not in st.session_state:
        st.session_state['confirm_password'] = ''

    # Input fields using session state
    name = st.text_input("Enter your name:", value=st.session_state['name'])
    age = st.number_input("Enter your age:", value=st.session_state['age'])
    sex = st.radio("Select Your Sex", ["Male", "Female"], index=["Male", "Female"].index(st.session_state['sex']))
    job_field = st.selectbox("What is your Job field", ('Academic', 'IT', 'Real Estate Business', 'Local Business', 'Salesman', 'Manager', 'Medical'), index=('Academic', 'IT', 'Real Estate Business', 'Local Business', 'Salesman', 'Manager', 'Medical').index(st.session_state['job_field']))
    dob = st.date_input("When's your birthday", value=st.session_state['dob'])
    user_image = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    email = st.text_input("Enter your E-Mail address", value=st.session_state['email'])
    password = st.text_input("Create your password", type="password", value=st.session_state['password'])
    confirm_password = st.text_input("Re-enter your password", type="password", value=st.session_state['confirm_password'])

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match. Please re-enter matching passwords.")
        else:
            # Process registration and save data
            expenses1.append({"name": name, "age": age, "sex": sex, "dob": str(dob), "job_field": job_field, "image": user_image})
            expenses2.append({"email": email, "password": hash_password(password)})
            save_details(file_name1, expenses1)
            save_details(file_name2, expenses2)
            st.success("Successfully Registered")

            # Resetting all the session state values
            st.session_state['name'] = ''
            st.session_state['age'] = 0
            st.session_state['sex'] = 'Male'
            st.session_state['job_field'] = 'Academic'
            st.session_state['dob'] = None
            st.session_state['user_image'] = None
            st.session_state['email'] = ''
            st.session_state['password'] = ''
            st.session_state['confirm_password'] = ''

def login_page():
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_login(email, password, "email_password_data.json"):
            st.success("Login successful!")
            show_matching_page('user_data.json')
        else:
            st.error("Invalid email or password")

def developer_page():
    st.header("Login As Admin")
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
        with open("user_data.json", "r") as file:
            st.download_button(label="Download JSON", data=file, file_name="user_data.json", mime="application/json")

if __name__ == "__main__":
    main()
