import streamlit as st
import io
from PIL import Image
import google.generativeai as genai
import os
import datetime
import sys

# Ensure parent directory is in path so we can import firebase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebase_utils import get_projects, update_project_status, add_activity


def process_images_with_gemini(before_img, after_img):
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            st.error("⚠️ GEMINI_API_KEY environment variable not set. Please set it to use the AI Audit.")
            return None
        
        genai.configure(api_key=api_key)
        
        # Load the Gemini 1.5 Flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        You are an AI auditor for a city infrastructure project (Project Gali-Pragati). 
        You have been provided two images: a 'Before' image showing an issue (e.g., pothole, broken streetlight) 
        and an 'After' image showing the claimed completed work.
        
        Please perform the following analysis:
        1. Confirm if both images appear to be of the exact same physical location based on surrounding landmarks, textures, or structures.
        2. Check if the requested work appears to be completed in the 'After' image compared to the 'Before' image.
        
        Respond with a formal 'Verification Certificate' including:
        - Location Match Assessment: (Pass/Fail + brief reason)
        - Work Completion Assessment: (Pass/Fail + brief reason)
        - Final Verdict: (APPROVED / REJECTED)
        - Confidence Level: (High/Medium/Low)
        """
        
        # Convert uploaded files to PIL Images for Gemini
        before_pil = Image.open(before_img)
        after_pil = Image.open(after_img)
        
        # Call the model
        response = model.generate_content([prompt, before_pil, after_pil])
        return response.text
        
    except Exception as e:
        st.error(f"Error communicating with Gemini API: {e}")
        return None


def render_ai_audit():
    st.markdown("Upload structural images before and after the fix.")
    
    projects = get_projects()
    pending_projects = [p for p in projects if p.get('status', '').lower() in ['yellow', 'red', 'pending']]
    project_options = {p['id']: f"{p['id']} - {p['title']} ({p.get('status')})" for p in pending_projects}
    
    if not project_options:
        st.info("No projects currently pending verification.")
        selected_project_id = None
    else:
        selected_project_id = st.selectbox("Select Project to Verify", options=list(project_options.keys()), format_func=lambda x: project_options[x])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📷 Before Fix")
        before_file = st.file_uploader("Upload Before Image", type=["jpg", "jpeg", "png"], key="before")
        if before_file:
            st.image(before_file, use_container_width=True)
            
    with col2:
        st.markdown("### 📷 After Fix")
        after_file = st.file_uploader("Upload After Image", type=["jpg", "jpeg", "png"], key="after")
        if after_file:
            st.image(after_file, use_container_width=True)
            
    if before_file and after_file and selected_project_id:
        st.markdown("---")
        if st.button("🔍 Verify Work Completion", type="primary"):
            with st.spinner("Analyzing structural changes using Gemini 1.5 Flash..."):
                result = process_images_with_gemini(before_file, after_file)
                
            if result:
                st.success("Analysis Complete!")
                st.markdown("### 📜 Automated Verification Certificate")
                st.info(f"**Timestamp:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(result)
                
                # Check if VERDICT is APPROVED
                if "APPROVED" in result:
                    st.balloons()
                    update_project_status(selected_project_id, "Green", "green")
                    add_activity(
                        icon="🤖", 
                        message=f"<strong>AI Verification:</strong> Project ({selected_project_id}) Approved. Status changed to Green.", 
                        time_ago="JUST NOW"
                    )
                    st.success(f"Project **{selected_project_id}** updated to Green status in database.")
                elif "REJECTED" in result:
                    update_project_status(selected_project_id, "Red", "red")
                    add_activity(
                        icon="❌", 
                        message=f"<strong>AI Verification Failed:</strong> Project ({selected_project_id}) Rejected. Status changed to Red.", 
                        time_ago="JUST NOW"
                    )
                    st.error(f"Project **{selected_project_id}** verification failed. Status updated to Red.")
