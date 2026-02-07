# attendance_system/chatbot.py

import streamlit as st
import google.generativeai as genai
import database as db
import pandas as pd

# Configure Gemini API
try:
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    st.info("Please make sure you have set up your GEMINI_API_KEY in .streamlit/secrets.toml")
    model = None

def get_gemini_response(prompt):
    """Sends a prompt to the Gemini API and gets a response."""
    if not model:
        return "Gemini model is not configured. Please check the API key."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while fetching response from Gemini: {e}"

def render_chatbot():
    """Renders a powerful chatbot using Gemini API and local database context."""
    with st.sidebar:
        with st.expander("🤖 College Assistant Chatbot", expanded=True):
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you today?"}]

            # Display chat messages
            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

            # User-provided prompt
            if prompt := st.chat_input("Ask me anything..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)

                # Check if the question is about personal attendance
                if any(keyword in prompt.lower() for keyword in ["attendance", "mera record", "meri حاضری"]):
                    # This is a personal data question
                    user_info = st.session_state.get('user_info')
                    if st.session_state.get('role') == 'Student' and user_info:
                        student_id = user_info['student_id']
                        # Fetch attendance data from our SQLite database
                        records = db.get_attendance_by_student(student_id)
                        if not records:
                            context_data = "No attendance records found for this student."
                        else:
                            df = pd.DataFrame([dict(r) for r in records])
                            total_classes = len(df)
                            present_count = (df['status'] == 'Present').sum()
                            percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
                            # Create a clean context string for the LLM
                            context_data = (f"Total classes: {total_classes}, "
                                            f"Classes attended: {present_count}, "
                                            f"Attendance Percentage: {percentage:.2f}%. "
                                            f"Recent records: {df.head(3).to_string(index=False)}")

                        # Create a specific prompt for Gemini with the fetched context
                        final_prompt = f"""
                        You are a helpful college assistant chatbot.
                        A student is asking about their attendance.
                        Their question is: "{prompt}"
                        
                        Here is their attendance data from the college database:
                        ---
                        {context_data}
                        ---
                        
                        Based on this data, please answer their question in a friendly and helpful tone (in Hinglish).
                        """
                        response = get_gemini_response(final_prompt)
                    else:
                        response = "Attendance data is only available for logged-in students. Please log in as a student to check."

                else:
                    # This is a general knowledge question
                    # We can add more context to guide the model
                    general_prompt = f"""
                    You are a helpful college assistant chatbot for a college in Jaipur, India in the year 2025.
                    A user has asked the following question: "{prompt}"
                    Please provide a helpful and concise answer.
                    """
                    response = get_gemini_response(general_prompt)
                
                # Add assistant's response to chat history and display it
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.chat_message("assistant").write(response)
