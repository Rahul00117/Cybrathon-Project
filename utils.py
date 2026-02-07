import streamlit as st
import pandas as pd
from PIL import Image
import os
from datetime import datetime
import face_recognition
import numpy as np

import database as db
from config import ID_YEAR_PREFIX, TEACHER_ID_PREFIX, STUDENT_ID_PREFIX, STUDENT_IMAGES_DIR, GROUP_PHOTOS_DIR

# --- ID Generation ---
def generate_id(user_type):
    """Generates a new sequential ID for a teacher or student."""
    if user_type == 'teacher':
        serial_key = 'last_teacher_serial'
        prefix = TEACHER_ID_PREFIX
    elif user_type == 'student':
        serial_key = 'last_student_serial'
        prefix = STUDENT_ID_PREFIX
    else:
        raise ValueError("Invalid user type.")
    
    next_serial = db.get_next_serial(serial_key)
    return f"{prefix}{ID_YEAR_PREFIX}{str(next_serial).zfill(4)}"

# --- File Handling ---
def save_image(uploaded_file, save_path):
    """Saves an uploaded image file."""
    try:
        img = Image.open(uploaded_file)
        img.save(save_path)
        return True
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return False

def generate_group_photo_path(teacher_id):
    """Generates a unique path for a group photo."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{teacher_id}_{timestamp}.jpg"
    return GROUP_PHOTOS_DIR / filename

# --- Face Recognition Logic (Using face_recognition library) ---

def recognize_from_group_photo(group_photo_path):
    """Recognizes students from a group photo using dlib/face_recognition."""
    # 1. Group photo load karein
    group_image = face_recognition.load_image_file(str(group_photo_path))
    
    # 2. Encodings nikaalein
    face_locations = face_recognition.face_locations(group_image, model="hog")
    group_face_encodings = face_recognition.face_encodings(group_image, face_locations)

    if not group_face_encodings:
        st.warning("No faces detected in the photo.")
        return []

    # 3. Students list fetch karein
    students = db.list_students()
    recognized_ids = []

    # 4. Comparison loop
    for group_encoding in group_face_encodings:
        for student in students:
            # FIX: student.get() ki jagah student['key'] use kiya
            try:
                student_img_path = student['photo_path']
                if not student_img_path or not os.path.exists(student_img_path):
                    continue
                
                reg_image = face_recognition.load_image_file(student_img_path)
                reg_encodings = face_recognition.face_encodings(reg_image)

                if reg_encodings:
                    matches = face_recognition.compare_faces([reg_encodings[0]], group_encoding, tolerance=0.5)
                    if matches[0]:
                        recognized_ids.append(student['student_id'])
            except Exception as e:
                print(f"Error processing student: {e}")
                continue
    
    return list(set(recognized_ids))

# --- Data Conversion ---
def to_csv(df):
    """Converts a DataFrame to a CSV string."""
    return df.to_csv(index=False).encode('utf-8')