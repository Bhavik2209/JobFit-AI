import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime
from analysis import get_match_analysis, get_resume_enhancement_suggestions
from display import display_match_results, display_enhancement_suggestions, display_linkedin_optimization
from utils import extract_text_from_pdf
from linkedin_optimization import generate_linkedin_optimization
from cover_letter import generate_custom_cover_letter
from layout_analysis import analyze_resume_layout

# Constants
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TOOL_OPTIONS = {
    "Basic Analysis": "📊",
    "Resume Enhancement": "🚀",
    "Layout Analysis": "📋",
    "Cover Letter Generator": "📨",
    "LinkedIn Optimization": "💼"
}

EMOJI_MAP = {
    "skills_match": "🎯",
    "experience_match": "⚡",
    "education_match": "🎓",
    "improvement_areas": "💡",
    "layout_score": "📐",
    "keyword_match": "🔍",
    "overall_match": "⭐"
}

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Error handling wrapper
def safe_analysis(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            return None
    return wrapper

def show_analysis_progress():
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = [
        ("Extracting Content", 0.2),
        ("Analyzing Format", 0.4),
        ("Comparing Requirements", 0.6),
        ("Generating Insights", 0.8),
        ("Finalizing Results", 1.0)
    ]
    
    for stage, progress in stages:
        status_text.text(f"🔄 {stage}...")
        progress_bar.progress(progress)
        time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()

def init_session_state():
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

def main():
    # Initialize session state
    init_session_state()

    # Page Configuration
    st.set_page_config(
        page_title="JobFit AI - Advanced Resume Analyzer",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    # Enhanced CSS Styling
    st.markdown("""
        <style>
        /* Global Styles */
        .main > div {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Button Styles - Using Streamlit's primary color */
        .stButton>button {
            height: 3rem;
            font-size: 1.2rem;
            transition: transform 0.2s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
        }
        
        /* Cards with subtle blue tints that work in both modes */
        .analysis-card {
            background: rgba(100, 149, 237, 0.05);  /* Very subtle blue tint */
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid rgba(100, 149, 237, 0.2);
            margin-bottom: 1rem;
        }
        
        /* File Upload Area */
        .uploadedFile {
            border: 2px dashed rgba(100, 149, 237, 0.5);
            border-radius: 10px;
            padding: 20px;
        }
        
        /* Feature Cards */
        .feature-card {
            background: rgba(100, 149, 237, 0.05);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(100, 149, 237, 0.2);
            transition: transform 0.2s;
        }
        .feature-card:hover {
            transform: translateY(-2px);
            background: rgba(100, 149, 237, 0.1);
        }
        
        /* Alerts with subtle backgrounds */
        .alert {
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .success {
            background: rgba(72, 187, 120, 0.1);
            border: 1px solid rgba(72, 187, 120, 0.2);
        }
        
        .warning {
            background: rgba(247, 174, 66, 0.1);
            border: 1px solid rgba(247, 174, 66, 0.2);
        }
        
        .error {
            background: rgba(245, 101, 101, 0.1);
            border: 1px solid rgba(245, 101, 101, 0.2);
        }

        /* Footer Styling */
        .footer {
            text-align: center;
            padding: 20px;
            background: rgba(100, 149, 237, 0.05);
            border-radius: 10px;
            margin-top: 30px;
            border: 1px solid rgba(100, 149, 237, 0.2);
        }
        
        /* Social Links */
        .social-link {
            display: inline-flex;
            align-items: center;
            padding: 8px 15px;
            border-radius: 20px;
            background: rgba(100, 149, 237, 0.1);
            border: 1px solid rgba(100, 149, 237, 0.2);
            margin: 0 10px;
            text-decoration: none;
            transition: transform 0.2s, background 0.2s;
        }
        
        .social-link:hover {
            transform: translateY(-2px);
            background: rgba(100, 149, 237, 0.15);
        }
        
        .social-link img {
            margin-right: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h1 style='color: white;'>🎯 JobFit AI</h1>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Analysis Tools")
        
        tool_selection = st.radio(
            "Select Analysis Type",
            options=list(TOOL_OPTIONS.keys()),
            format_func=lambda x: f"{TOOL_OPTIONS[x]} {x}",
            help="Choose the type of analysis you want to perform"
        )
        
        st.divider()
        
        st.markdown("""
            <div class='feature-card'>
                <h3>🔍 About JobFit AI</h3>
                <ul>
                    <li>Match resumes to job descriptions</li>
                    <li>Get enhancement suggestions</li>
                    <li>Analyze resume layout</li>
                    <li>Generate custom cover letters</li>
                    <li>Optimize LinkedIn profiles</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Main Content Area
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1>🎯 JobFit AI - Advanced Resume Analyzer</h1>
            <p style='color: #6B7280;'>Your AI-powered career advancement assistant</p>
        </div>
    """, unsafe_allow_html=True)

    # Input Section with Enhanced UI
    input_col1, input_col2 = st.columns([1, 1])

    with input_col1:
        st.markdown("""
            <div class='analysis-card'>
                <h3>📝 Job Description</h3>
            </div>
        """, unsafe_allow_html=True)
        job_description = st.text_area(
            label="Paste the job description here",
            height=200,
            placeholder="Copy and paste the complete job description text here...",
            help="The more detailed the job description, the better the analysis"
        )

    with input_col2:
        st.markdown("""
            <div class='analysis-card'>
                <h3>📄 Resume Upload</h3>
            </div>
        """, unsafe_allow_html=True)
        resume_file = st.file_uploader(
            "Upload your resume (PDF format)",
            type=['pdf'],
            help="Only PDF files are supported at this time"
        )
        
        if resume_file:
            st.success("✅ Resume uploaded successfully!")
            try:
                resume_text = extract_text_from_pdf(resume_file)
                st.info("📄 Resume text extracted successfully")
            except Exception as e:
                st.error(f"❌ Error extracting text from PDF: {str(e)}")

    # Analysis Button
    st.markdown("---")
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
    with analyze_col2:
        analyze_button = st.button(
            "🔍 Analyze Resume",
            type="primary",
            use_container_width=True,
        )

    # Results Section with Progress Tracking
    if analyze_button and resume_file:
        try:
            with st.spinner('🔄 Analyzing your resume...'):
                show_analysis_progress()
                
                @safe_analysis
                def perform_analysis():
                    if tool_selection == "Basic Analysis":
                        if job_description:
                            st.markdown("""
                                <div class='analysis-card'>
                                    <h3>📊 Analysis Results</h3>
                                </div>
                            """, unsafe_allow_html=True)
                            analysis = get_match_analysis(model, job_description, resume_text)
                            display_match_results(analysis)
                            return analysis
                        else:
                            st.warning("⚠️ Please enter a job description for analysis.")
                    
                    elif tool_selection == "Resume Enhancement":
                        st.markdown("""
                            <div class='analysis-card'>
                                <h3>🚀 Enhancement Suggestions</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        enhancements = get_resume_enhancement_suggestions(model, resume_text)
                        display_enhancement_suggestions(enhancements)
                        return enhancements
                    
                    elif tool_selection == "Layout Analysis":
                        st.markdown("""
                            <div class='analysis-card'>
                                <h3>📋 Layout Analysis</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        layout_analysis = analyze_resume_layout(resume_file)
                        if layout_analysis:
                            score_col, issues_col = st.columns([1, 2])
                            with score_col:
                                st.metric(
                                    "Formatting Score",
                                    f"{layout_analysis['formatting_score']}%"
                                )
                            with issues_col:
                                if layout_analysis["layout_issues"]:
                                    st.warning("Layout Issues Found:")
                                    for issue in layout_analysis["layout_issues"]:
                                        st.markdown(f"- ⚠️ {issue}")
                                else:
                                    st.success("✅ No major layout issues found")
                            return layout_analysis
                    
                    elif tool_selection == "Cover Letter Generator":
                        if job_description:
                            st.markdown("""
                                <div class='analysis-card'>
                                    <h3>📨 Custom Cover Letter</h3>
                                </div>
                            """, unsafe_allow_html=True)
                            cover_letter = generate_custom_cover_letter(
                                model,
                                job_description,
                                resume_text
                            )
                            if cover_letter:
                                st.markdown(cover_letter)
                                st.download_button(
                                    "📥 Download Cover Letter",
                                    cover_letter,
                                    file_name="cover_letter.txt"
                                )
                            return cover_letter
                        else:
                            st.warning("⚠️ Please enter a job description for cover letter generation.")
                    
                    elif tool_selection == "LinkedIn Optimization":
                        st.markdown("""
                            <div class='analysis-card'>
                                <h3>💼 LinkedIn Profile Optimization</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        linkedin_suggestions = generate_linkedin_optimization(
                            model,
                            resume_text
                        )
                        display_linkedin_optimization(linkedin_suggestions)
                        return linkedin_suggestions

                results = perform_analysis()
                if results:
                    st.session_state.analysis_history.append({
                        'timestamp': datetime.now(),
                        'type': tool_selection,
                        'results': results
                    })

        except Exception as e:
            st.error("❌ An error occurred during analysis. Please try again.")
            st.error(f"Error details: {str(e)}")

    elif analyze_button:
        st.warning("⚠️ Please upload a resume PDF to begin analysis.")

    # Enhanced Footer
    st.markdown("---")
    st.markdown("""
        <div class='footer'>
            <p style='margin-bottom: 15px; font-size: 16px;'>Made with 🤖✨ by JobFit AI</p>
            <div style='display: flex; justify-content: center; gap: 20px;'>
                <a href="https://www.linkedin.com/in/bhavik-rohit" target="_blank" class="social-link">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" 
                         width="20" height="20">
                    Connect on LinkedIn
                </a>
                <a href="https://github.com/Bhavik2209" target="_blank" class="social-link">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" 
                         width="20" height="20">
                    View on GitHub
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()