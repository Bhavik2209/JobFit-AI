import json
import streamlit as st

def get_match_analysis(model, job_description, resume_text):
    prompt = f"""
    Act as an expert ATS (Applicant Tracking System) scanner and professional resume analyst. Analyze the job description and resume provided below.
    
    Return ONLY the following JSON format with no additional text, comments, or markdown formatting:

    {{
        "overall_match": <number between 0-100>,
        "keyword_match_score": <number between 0-100>,
        "categories": {{
            "technical_skills": {{
                "match": <number between 0-100>,
                "present_skills": [<list of matching technical skills found>],
                "missing_skills": [<list of required technical skills not found>],
                "improvement_suggestions": [<detailed suggestions for improving technical skills section>]
            }},
            "soft_skills": {{
                "match": <number between 0-100>,
                "present_skills": [<list of matching soft skills found>],
                "missing_skills": [<list of required soft skills not found>],
                "improvement_suggestions": [<detailed suggestions for improving soft skills section>]
            }},
            "experience": {{
                "match": <number between 0-100>,
                "strengths": [<list of strong experience points matching job requirements>],
                "gaps": [<list of experience gaps compared to requirements>],
                "improvement_suggestions": [<detailed suggestions for improving experience section>]
            }},
            "education": {{
                "match": <number between 0-100>,
                "relevant_qualifications": [<list of relevant educational qualifications>],
                "improvement_suggestions": [<suggestions for education section>]
            }}
        }},
        "ats_optimization": {{
            "formatting_issues": [<list of ATS formatting issues found>],
            "keyword_optimization": [<suggestions for better keyword placement>],
            "section_improvements": [<suggestions for improving section organization>]
        }},
        "impact_scoring": {{
            "achievement_metrics": <number between 0-100>,
            "action_verbs": <number between 0-100>,
            "quantifiable_results": <number between 0-100>,
            "improvement_suggestions": [<detailed suggestions for improving impact statements>]
        }}
    }}

    Job Description: {job_description}

    Resume: {resume_text}
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up the response text
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        # Additional cleaning to handle potential formatting issues
        response_text = response_text.replace('\n', ' ').replace('\r', '')
        response_text = ' '.join(response_text.split())
        
        # Try to find the JSON object boundaries
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            json_str = response_text[start_idx:end_idx]
            try:
                analysis = json.loads(json_str)
                
                # Validate required fields
                required_fields = ['overall_match', 'keyword_match_score', 'categories', 'ats_optimization', 'impact_scoring']
                if not all(field in analysis for field in required_fields):
                    raise ValueError("Missing required fields in the analysis")
                
                return analysis
            except json.JSONDecodeError as je:
                st.error(f"JSON parsing error: {str(je)}")
                st.error("Raw JSON string:")
                st.code(json_str)
                raise
        else:
            raise ValueError("Could not find valid JSON in the response")
            
    except Exception as e:
        st.error("Error in analysis. Retrying with simplified prompt...")
        
        # Fallback to simplified analysis if the detailed one fails
        try:
            simplified_prompt = f"""
            Analyze the job description and resume below. Return ONLY a JSON object in this exact format:
            {{
                "overall_match": <number>,
                "keyword_match_score": <number>,
                "categories": {{
                    "technical_skills": {{"match": <number>, "present_skills": [], "missing_skills": [], "improvement_suggestions": []}},
                    "soft_skills": {{"match": <number>, "present_skills": [], "missing_skills": [], "improvement_suggestions": []}},
                    "experience": {{"match": <number>, "strengths": [], "gaps": [], "improvement_suggestions": []}},
                    "education": {{"match": <number>, "relevant_qualifications": [], "improvement_suggestions": []}}
                }},
                "ats_optimization": {{"formatting_issues": [], "keyword_optimization": [], "section_improvements": []}},
                "impact_scoring": {{"achievement_metrics": <number>, "action_verbs": <number>, "quantifiable_results": <number>, "improvement_suggestions": []}}
            }}

            Job Description: {job_description}
            Resume: {resume_text}
            """
            
            retry_response = model.generate_content(simplified_prompt)
            retry_text = retry_response.text.strip()
            retry_text = retry_text.replace('```json', '').replace('```', '').strip()
            
            start_idx = retry_text.find('{')
            end_idx = retry_text.rfind('}') + 1
            json_str = retry_text[start_idx:end_idx]
            
            return json.loads(json_str)
            
        except Exception as retry_error:
            st.error(f"Retry failed: {str(retry_error)}")
            raise

def get_resume_enhancement_suggestions(model, resume_text):
    """Get resume enhancement suggestions"""
    prompt = f"""
    Analyze this resume and provide specific enhancement suggestions. Return ONLY a JSON object in this exact format, with no additional text or formatting:
    {{
        "summary_section": {{
            "has_summary": true,
            "suggestions": ["suggestion1", "suggestion2"],
            "sample_summary": "A professional summary example"
        }},
        "bullet_points": {{
            "strength": 75,
            "weak_bullets": ["weak bullet 1", "weak bullet 2"],
            "improved_versions": ["improved version 1", "improved version 2"]
        }},
        "power_verbs": {{
            "current_verbs": ["current1", "current2"],
            "suggested_verbs": ["suggested1", "suggested2"]
        }},
        "technologies": {{
            "mentioned": ["tech1", "tech2"],
            "suggested_additions": ["suggestion1", "suggestion2"]
        }},
        "certifications": {{
            "relevant_certs": ["cert1", "cert2"],
            "priority_order": ["priority1", "priority2"]
        }}
    }}

    Resume text: {resume_text}
    """
    
    try:
        response = model.generate_content(prompt)
        return clean_and_parse_json(response.text)
    except Exception as e:
        st.error(f"Error in enhancement analysis: {str(e)}")
        return None

def clean_and_parse_json(response_text):
    """Clean the response text and parse it as JSON"""
    # Remove any markdown code block markers
    cleaned_text = response_text.replace('```json', '').replace('```', '').strip()
    
    # Try to find JSON boundaries
    start_idx = cleaned_text.find('{')
    end_idx = cleaned_text.rfind('}') + 1
    
    if start_idx != -1 and end_idx > 0:
        json_str = cleaned_text[start_idx:end_idx]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            st.error(f"JSON parsing error: {str(e)}")
            st.code(json_str)  # Display the problematic JSON for debugging
            return None
    return None