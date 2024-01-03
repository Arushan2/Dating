import streamlit as st
import json
import os
import hashlib
import base64
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
            return user  # Return the user data
    return None


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

def show_user_details(user):
    if user and 'name' in user:
        st.title(f"Welcome, {user['name']}")
        # if 'image' in user and user['image']:  # Check if image key exists and is not None
        #     st.image(user['image'], caption='Profile Picture', use_column_width=True)
        st.text(f"Name: {user['name']}")
        st.text(f"Age: {user.get('age', 'Not provided')}")
        st.text(f"Sex: {user.get('sex', 'Not provided')}")
        st.text(f"Job Field: {user.get('job_field', 'Not provided')}")
        st.text(f"Email: {user.get('email', 'Not provided')}")
        # Add more details as needed
    else:
        st.error("User details not found.")




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
    users = load_details(file_name1)
    credentials = load_details(file_name2)

    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", value=None)
    sex = st.radio("Select Your Sex", ["Male", "Female"])
    job_field = st.selectbox("What is your Job field", ('Academic', 'IT', 'Real Estate Business', 'Local Business', 'Salesman', 'Manager', 'Medical'))
    dob = st.date_input("When's your birthday")
    user_image = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
    email = st.text_input("Enter your E-Mail address")
    password = st.text_input("Create your password", type="password")
    confirm_password = st.text_input("Re-enter your password", type="password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match. Please re-enter matching passwords.")
        else:
            image_string = base64.b64encode(user_image.getvalue()).decode() if user_image else None
            users.append({"name": name, "age": age, "sex": sex, "dob": str(dob), "job_field": job_field, "image": image_string ,"email":email})
            credentials.append({"email": email, "password": hash_password(password)})
            save_details(file_name1, users)
            save_details(file_name2, credentials)
            st.success("Successfully Registered")

def login_page():
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        logged_in_email = verify_login(email, password, "email_password_data.json")
        if logged_in_email:
            st.success("Login successful!")
            # Find the user details
            user = find_user_by_email(email, "user_data.json")  # Corrected file name here
            if user:
                show_user_details(user)
            else:
                st.error("User details not found.")
        else:
            st.error("Invalid email or password")


def find_user_by_email(email, file_name):
    users = load_details(file_name)
    for user in users:
        if user.get('email') == email:
            return user
    return None



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
