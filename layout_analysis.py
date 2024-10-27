import PyPDF2
import streamlit as st

def analyze_resume_layout(pdf_file):
    layout_issues = []
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        if num_pages > 2:
            layout_issues.append("Resume exceeds recommended 1-2 page length")
            
        return {
            "num_pages": num_pages,
            "layout_issues": layout_issues,
            "formatting_score": 100 - (len(layout_issues) * 10)  # Simple scoring system
        }
    except Exception as e:
        st.error(f"Error analyzing layout: {str(e)}")
        return None