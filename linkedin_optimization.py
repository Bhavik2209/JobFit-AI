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

def generate_linkedin_optimization(model, resume_text):
    """Generate LinkedIn profile optimization suggestions"""
    prompt = f"""
    Analyze this resume and provide LinkedIn optimization suggestions. Return ONLY a JSON object in this exact format, with no additional text or formatting:
    {{
        "headline_suggestions": ["headline1", "headline2", "headline3"],
        "about_section": "Suggested about section content",
        "key_achievements": ["achievement1", "achievement2", "achievement3"],
        "skills_to_add": ["skill1", "skill2", "skill3"],
        "profile_optimization": ["tip1", "tip2", "tip3"],
        "basic tips and suggestions": ["tip1", "tip2", "tip3"]
    }}

    Resume: {resume_text}
    """
    
    try:
        response = model.generate_content(prompt)
        result = clean_and_parse_json(response.text)
        if result is None:
            # If parsing fails, try a simplified prompt
            simplified_prompt = f"""
            Analyze this resume and provide LinkedIn optimization suggestions. Return ONLY a JSON object with these keys:
            headline_suggestions, about_section, key_achievements, skills_to_add, profile_optimization.
            Keep it simple and ensure it's valid JSON.

            Resume: {resume_text}
            """
            retry_response = model.generate_content(simplified_prompt)
            result = clean_and_parse_json(retry_response.text)
        
        return result
    except Exception as e:
        st.error(f"Error generating LinkedIn optimization: {str(e)}")
        return None
