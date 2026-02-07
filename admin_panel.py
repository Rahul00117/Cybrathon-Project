# attendance_system/admin_panel.py (Updated Code with Passwords in List)

import streamlit as st
import pandas as pd
import database as db
import utils
from config import STUDENT_IMAGES_DIR

def admin_dashboard():
    """UI for the admin dashboard with delete functionality and password visibility."""
    st.title("Admin Dashboard ⚙️")
    
    tabs = st.tabs(["Register Teacher", "Register Student", "View & Manage Users"])
    
    with tabs[0]:
        st.subheader("Register New Teacher")
        with st.form("teacher_reg_form", clear_on_submit=True):
            name = st.text_input("Name")
            email = st.text_input("Email")
            branch = st.text_input("Branch")
            subject = st.text_input("Subject")
            submitted = st.form_submit_button("Register Teacher")
            
            if submitted:
                if all([name, email, branch, subject]):
                    teacher_id = utils.generate_id('teacher')
                    password = teacher_id # Auto-generated password
                    success = db.create_teacher(teacher_id, name, email, branch, subject, password)
                    if success:
                        st.success(f"✅ Teacher Registered Successfully!")
                        st.info(f"**Teacher ID:** `{teacher_id}`")
                        st.info(f"**Password:** `{password}` (Please share this with the teacher)")
                    else:
                        st.error("❌ Email already exists.")
                else:
                    st.warning("⚠️ Please fill all fields.")
    
    with tabs[1]:
        st.subheader("Register New Student")
        with st.form("student_reg_form", clear_on_submit=True):
            name = st.text_input("Name")
            roll = st.text_input("Roll Number")
            section = st.text_input("Section")
            _class = st.text_input("Class")
            photo = st.file_uploader("Upload Student's Face Photo", type=['jpg', 'png', 'jpeg'])
            submitted = st.form_submit_button("Register Student")

            if submitted:
                if all([name, roll, section, _class, photo]):
                    student_id = utils.generate_id('student')
                    password = student_id # Auto-generated password
                    photo_path = STUDENT_IMAGES_DIR / f"{student_id}.jpg"
                    
                    if utils.save_image(photo, photo_path):
                        db.create_student(student_id, name, roll, section, _class, password, str(photo_path))
                        st.success(f"✅ Student Registered Successfully!")
                        st.info(f"**Student ID:** `{student_id}`")
                        st.info(f"**Password:** `{password}` (Please share this with the student)")
                        st.image(photo, caption=f"Photo for {name}", width=150)
                else:
                    st.warning("⚠️ Please fill all fields, including the photo.")

    with tabs[2]:
        st.subheader("Registered Users Management")
        
        st.write("#### Teachers List")
        teachers = db.list_teachers()
        if teachers:
            # Column headers
            cols = st.columns([2, 2, 2, 3, 1])
            cols[0].write("**Name**")
            cols[1].write("**Teacher ID**")
            cols[2].write("**Password**")
            cols[3].write("**Email**")
            cols[4].write("**Action**")

            # Har teacher ke liye details, password aur delete button dikhayein
            for teacher in teachers:
                cols = st.columns([2, 2, 2, 3, 1])
                cols[0].write(teacher['name'])
                cols[1].write(f"`{teacher['teacher_id']}`")
                # Kyunki password ID ke barabar hai, hum ID ko hi password ki jagah dikha rahe hain
                cols[2].write(f"`{teacher['teacher_id']}`") 
                cols[3].write(teacher['email'])
                if cols[4].button("Delete 🗑️", key=f"del_teacher_{teacher['teacher_id']}", type="primary"):
                    db.delete_teacher(teacher['teacher_id'])
                    st.success(f"Teacher {teacher['name']} ({teacher['teacher_id']}) has been removed.")
                    st.rerun()
        else:
            st.info("No teachers registered.")

        st.write("---") # Divider
        st.write("#### Students List")
        students = db.list_students()
        if students:
            # Column headers
            cols = st.columns([2, 2, 2, 2, 1])
            cols[0].write("**Name**")
            cols[1].write("**Student ID**")
            cols[2].write("**Password**")
            cols[3].write("**Class**")
            cols[4].write("**Action**")
            
            # Har student ke liye details, password aur delete button 
            for student in students:
                cols = st.columns([2, 2, 2, 2, 1])
                cols[0].write(student['name'])
                cols[1].write(f"`{student['student_id']}`")
                # Kyunki password ID ke barabar hai, hum ID ko hi password ki jagah dikha rahe hain
                cols[2].write(f"`{student['student_id']}`")
                cols[3].write(student['class'])
                if cols[4].button("Delete 🗑️", key=f"del_student_{student['student_id']}", type="primary"):
                    db.delete_student(student['student_id'])
                    st.success(f"Student {student['name']} ({student['student_id']}) has been removed.")
                    st.rerun()
        else:
            st.info("No students registered.")

# ### ## ⚠️ Ek Zaroori Security Note (Important Security Note)

# Main list me password likh  diya hai pr ye kuch baate hai jo security based hai-

# * **Real-world applications mein passwords ko is tarah list mein kabhi nahi dikhaya jaata.**
# * Yeh ek bada security risk hota hai. Agar koi admin ke peeche khada ho ya screen ka photo le le, to saare users ke account ki details compromise ho sakti hain.
# * Badi applications mein 'Password Dekhne' ki jagah **'Password Reset Karne'** ka button hota hai, jisse user ko ek naya password email par bhej diya jaata hai.

# jahan password aur ID ek hi hain, Par hamesha yaad rakhein ki asli projects mein password ko hamesha private rakhna hai.
