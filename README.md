# JobFit AI - Advanced Resume Analyzer

## Description
JobFit AI is an innovative resume analysis tool that leverages artificial intelligence to provide job seekers with valuable insights and recommendations. Our application helps users optimize their resumes, prepare for interviews, and explore career opportunities.

## Features
- Resume Analysis: Get detailed feedback on your resume's content and format.
- ATS Compatibility Check: Ensure your resume is optimized for Applicant Tracking Systems.
- Job Description Matching: Compare your resume against specific job descriptions.
- Career Story Generator: Craft a compelling narrative of your professional journey.
- Future Skills Predictor: Discover skills that will be crucial in your field in the coming years.
- Personal Brand Statement: Generate a unique value proposition statement.
- Interview Question Generator: Prepare for interviews with custom questions based on your resume.
- Career Pivot Advisor: Explore potential career transitions based on your skills.

- Provide feedback to help us improve the application.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/jobfit-ai.git
   cd jobfit-ai
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

Run the Streamlit app:
```
streamlit run main.py
```
