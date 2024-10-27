import streamlit as st

def generate_custom_cover_letter(model, job_description, resume_text):
    prompt = f"""
    Create a professional cover letter based on the job description and resume.
    Make it engaging and highlight relevant experience and skills.
    
    Job Description: {job_description}
    Resume: {resume_text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating cover letter: {str(e)}")
        return None