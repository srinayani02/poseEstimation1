import streamlit as st
import sqlite3
import os
import tempfile
import cv2
from pose_detector import PoseDetector

# Initialize DB
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    email TEXT,
    phone TEXT,
    gender TEXT,
    address TEXT
)''')
conn.commit()

# Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Registration
def register():
    st.title("User Registration")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        address = st.text_area("Address")
        submit = st.form_submit_button("Register")
        if submit:
            try:
                c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
                          (username, password, email, phone, gender, address))
                conn.commit()
                st.success("Registration successful!")
            except sqlite3.IntegrityError:
                st.error("Username already exists!")

# Login
def login():
    st.title("User Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            result = c.fetchone()
            if result:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid credentials")

# Pose Detection
def pose_estimation():
    st.title("Human Pose Tracking & Estimation")
    video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
    
    if video_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        video_path = tfile.name

        cap = cv2.VideoCapture(video_path)
        detector = PoseDetector()

        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = detector.findPose(frame)
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame, channels="RGB")

        cap.release()

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login", "Register", "Pose Estimation"])

if page == "Register":
    register()
elif page == "Login":
    login()
elif page == "Pose Estimation":
    if st.session_state.logged_in:
        pose_estimation()
    else:
        st.warning("Please login first.")
