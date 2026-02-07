# attendance_system/teacher_panel.py

import streamlit as st
import pandas as pd
from datetime import datetime
import database as db
import utils

def teacher_dashboard():
    """UI for the teacher dashboard."""
    user_info = st.session_state.user_info
    st.title(f"Welcome, {user_info['name']} 👋")

    tabs = st.tabs(["Profile", "Mark Attendance", "Group Photo Upload"])

    with tabs[0]:
        st.subheader("Your Profile")
        st.write(f"**Teacher ID:** {user_info['teacher_id']}")
        st.write(f"**Email:** {user_info['email']}")
        st.write(f"**Branch:** {user_info['branch']}")
        st.write(f"**Subject:** {user_info['subject']}")

    with tabs[1]:
        st.subheader("Mark Manual Attendance")
        students = db.list_students()
        if not students:
            st.warning("No students registered yet.")
            return

        date = st.date_input("Select Date", value=datetime.today())
        date_iso = date.isoformat()
        
        with st.form("attendance_form"):
            attendance_data = {}
            for student in students:
                cols = st.columns([3, 1, 1])
                cols[0].write(f"{student['name']} ({student['student_id']})")
                status = cols[1].radio("Status", ["Present", "Absent"], key=f"status_{student['student_id']}", horizontal=True, label_visibility="collapsed")
                attendance_data[student['student_id']] = status

            submitted = st.form_submit_button("Submit Attendance")
            if submitted:
                for student_id, status in attendance_data.items():
                    db.mark_attendance(student_id, user_info['subject'], date_iso, status, user_info['teacher_id'])
                st.success("Attendance marked successfully!")

    with tabs[2]:
        st.subheader("Upload Group Photo for Auto-Attendance")
        st.info("This feature will use AI to recognize students from the photo and mark their attendance automatically in the future.")
        group_photo = st.file_uploader("Upload a class group photo", type=['jpg', 'png', 'jpeg'])

        if group_photo:
            photo_path = utils.generate_group_photo_path(user_info['teacher_id'])
            if utils.save_image(group_photo, photo_path):
                st.success(f"Group photo saved successfully to {photo_path}")
                st.image(group_photo, caption="Uploaded Group Photo")
                
                # Placeholder for recognition logic
                with st.spinner("Analyzing photo for faces... (AI feature in development)"):
                    recognized_students = utils.recognize_from_group_photo(photo_path)
                    if recognized_students:
                        st.write("Recognized Students:", recognized_students)
                    else:
                        st.write("No students were automatically recognized in this demo.")