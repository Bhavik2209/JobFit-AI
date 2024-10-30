import streamlit as st
import json
import re
from analysis import clean_and_parse_json

def clean_and_parse_json(response_text):
    # Remove any non-JSON content
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        try:
            # Try to parse the JSON
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            st.error(f"JSON parsing error: {str(e)}")
            st.code(json_str)  # Display the problematic JSON for debugging
            return None
    else:
        st.error("No valid JSON found in the response")
        return None

def generate_interview_tips(model, resume_text):
    prompt = f"""
        Analyze this resume and provide interview preparation tips and possible questions to expect. Return ONLY a JSON object in this exact format, with no additional text or formatting:
        {{
            "preparation_tips": ["tip1", "tip2", "tip3"],
            "questions_to_expect": ["question1", "question2", "question3"],
            "behavioral_questions": ["question1", "question2", "question3"],
            "role_specific_questions": ["question1", "question2", "question3"],
            "general_interview_tips": ["tip1", "tip2", "tip3"]
        }}

        Resume: {resume_text}
        """
    try:
        response = model.generate_content(prompt)
        result = clean_and_parse_json(response.text)
        if result is None:
            # If parsing fails, try a simplified prompt
            simplified_prompt = f"""
                Analyze this resume and provide interview preparation tips. 
                Return ONLY a JSON object with these keys: preparation_tips, 
                questions_to_expect, behavioral_questions, role_specific_questions, 
                general_interview_tips. Keep it simple and ensure it's valid JSON.

                Resume: {resume_text}
                """

            retry_response = model.generate_content(simplified_prompt)
            result = clean_and_parse_json(retry_response.text)
        
        return result
    except Exception as e:
        st.error(f"Error generating LinkedIn optimization: {str(e)}")
        return None
