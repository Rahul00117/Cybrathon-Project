# attendance_system/main.py

import streamlit as st
import database as db
import auth
import admin_panel
import teacher_panel
import student_panel
import chatbot

st.set_page_config(page_title="College Attendance System", layout="centered")

def main():
    """Main function to run the Streamlit app."""
    # Initialize the database on the first run
    db.init_db()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.user_info = None

    # Main routing logic
    if st.session_state.logged_in:
        with st.sidebar:
            st.title("Navigation")
            user_name = st.session_state.user_info.get('name', st.session_state.user_info.get('email'))
            st.write(f"Welcome, **{user_name}**!")
            st.write(f"Role: **{st.session_state.role}**")
            if st.button("Logout", use_container_width=True, type="primary"):
                st.session_state.clear()
                st.rerun()

        # Render panels based on role
        if st.session_state.role == "Admin":
            admin_panel.admin_dashboard()
        elif st.session_state.role == "Teacher":
            teacher_panel.teacher_dashboard()
        elif st.session_state.role == "Student":
            student_panel.student_dashboard()
        
        # Render chatbot for logged-in users
        chatbot.render_chatbot()
        
    else:
        st.title("Welcome to the AI-Based Attendance System")
        st.image("https://www.gstatic.com/lamda/images/gemini/google_bard_logo_192px_clr_v002.svg", width=100)
        auth.login()

if __name__ == "__main__":
    main()