# attendance_system/student_panel.py

import streamlit as st
import pandas as pd
import database as db
import utils

def student_dashboard():
    """UI for the student dashboard."""
    user_info = st.session_state.user_info
    st.title(f"Welcome, {user_info['name']} 🎓")

    tabs = st.tabs(["Profile", "View Attendance"])

    with tabs[0]:
        st.subheader("Your Profile")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(user_info['photo_path'], width=150)
        with col2:
            st.write(f"**Student ID:** {user_info['student_id']}")
            st.write(f"**Roll Number:** {user_info['roll']}")
            st.write(f"**Class:** {user_info['class']}")
            st.write(f"**Section:** {user_info['section']}")

    with tabs[1]:
        st.subheader("Your Attendance Report")
        records = db.get_attendance_by_student(user_info['student_id'])
        if not records:
            st.info("No attendance records found.")
        else:
            df = pd.DataFrame([dict(r) for r in records])
            
            # Attendance Percentage
            total_classes = len(df)
            present_count = (df['status'] == 'Present').sum()
            percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
            
            st.metric(label="Overall Attendance", value=f"{percentage:.2f}%", delta=f"{present_count}/{total_classes} days present")
            st.progress(percentage / 100)

            st.dataframe(df, use_container_width=True, hide_index=True)

            csv = utils.to_csv(df)
            st.download_button(
                label="📥 Download Attendance as CSV",
                data=csv,
                file_name=f"{user_info['student_id']}_attendance.csv",
                mime="text/csv",
            )