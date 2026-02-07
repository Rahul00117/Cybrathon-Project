"# Cybrathon-Project" 
# AI-Based Face Recognition Attendance System

### Detect, Separate and Match Individuals from Group Photos using Face Recognition

---

## Project Overview

This project is an AI-powered Face Recognition Attendance System developed for college students.
The system automatically detects, separates, and matches individuals from a group photo and marks attendance subject-wise.

It includes:

* Admin (Teacher) Panel
* Student Panel
* AI Chatbot (Text + Voice Support)
* Group Photo & Live Attendance Detection
* Subject-wise Attendance Tracking
* Attendance Report Generation

The system is built using **Python, Streamlit, Flask, and Face Recognition techniques**.

---

## Objectives

* Automate attendance marking using AI-based face recognition
* Reduce manual errors in attendance tracking
* Maintain subject-wise attendance records
* Provide downloadable attendance reports
* Enable chatbot-based interaction for students and teachers
* Support live image capture & group photo attendance

---

## Tech Stack

| Technology        | Purpose                   |
| ----------------- | ------------------------- |
| Python            | Core Programming          |
| Streamlit         | Frontend UI               |
| Flask             | Backend API               |
| OpenCV            | Image Processing          |
| face_recognition  | Face Detection & Matching |
| SQLite/MySQL      | Database                  |
| SpeechRecognition | Voice Input               |
| Text-to-Speech    | Voice Output              |
| Pandas            | Data Handling             |

---

## Admin (Teacher) Features

* Register students with:

  * Name
  * Roll Number
  * Branch
  * Section
  * Photo
* Take group photo to mark attendance automatically
* Live camera attendance marking
* Define lecture duration (1 hour = 1 attendance entry)
* Subject-wise attendance management
* Download subject-wise attendance reports (restricted to their subject only)
* Query chatbot for:

  * Students below 75% attendance
  * Government schemes
  * Attendance-related queries

---

## Student Features

* Secure login system
* View subject-wise attendance
* Download/print attendance report
* View profile details
* Chatbot access (Text & Voice) for:

  * Attendance queries
  * Scholarship schemes
  * General academic information

---

## AI Chatbot Features

* Available for both Teachers and Students
* Supports:

  * Text queries
  * Voice queries
* Provides:

  * Attendance information
  * Low attendance alerts
  * Government scholarship schemes
  * Relevant academic responses

---

## Face Recognition System

* Detects multiple faces from group photos
* Matches detected faces with registered student database
* Marks attendance automatically
* Supports live camera-based attendance
* Maintains subject-wise attendance entries

---

## Subject-Wise Attendance Logic

* Each subject is handled separately
* Teachers can define lecture duration in hours
* Each hour = 1 attendance record
* Multiple teachers supported
* Teachers can only download attendance reports for subjects they teach

---

## Project Structure

```
AI-Face-Recognition-Attendance/
│
├── app.py                  # Streamlit Main Application
├── backend/
│   ├── routes.py
│   ├── database.py
│
├── models/
│   ├── face_encoding.pkl
│
├── dataset/
│   ├── student_images/
│
├── chatbot/
│   ├── chatbot_logic.py
│
├── utils/
│   ├── face_utils.py
│   ├── report_generator.py
│
├── requirements.txt
└── README.md
```

---

## Security & Access Control

* Role-based authentication (Admin & Student)
* Subject-wise report restriction
* Secure login system
* Controlled attendance access

---

## Future Enhancements

* Cloud deployment (AWS / Azure)
* Mobile application integration
* Real-time attendance dashboard
* QR-based backup attendance
* Advanced AI analytics & prediction
* Integration with college ERP systems

---

## Real-World Impact

* Saves time for teachers
* Prevents proxy attendance
* Ensures transparency
* AI-driven academic monitoring
* Improves attendance management efficiency

---

## Developer

**Rahul Prajapat**
B.Tech (Artificial Intelligence)
SKIT Jaipur

---

