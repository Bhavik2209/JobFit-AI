import streamlit as st

def display_match_results(analysis):
    # Updated CSS with theme-aware styles
    st.markdown("""
        <style>
        /* Global theme-aware text styles */
        .theme-aware-text {
            color: var(--text-color, inherit) !important;
        }
        
        /* Score card styles */
        .score-card {
            background: linear-gradient(135deg, #1e3799 0%, #0c2461 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .score-card h1, .score-card p, .score-card h3, .score-card h2 {
            color: white !important;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        
        /* Metric card styles */
        .metric-card {
            background: rgba(255, 255, 255, 0.1);
            
            backdrop-filter: blur(10px);
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem;
            text-align: center;
        }
        
        .metric-card h3, .metric-card h2 {
            text-align: center;
            margin: 0;
            padding: 0;
        }
        
        /* Category card styles */
        .category-card {
            background: var(--background-color, #ffffff);
            color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        /* Suggestion card styles */
        .suggestion-card {
            background-color: var(--background-color, #ffffff);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 0.5rem;
            border-left: 4px solid #3498db;
            color: var(--text-color, #000000);
        }
        
        /* Skills section styles */
        .skills-section {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            background: var(--background-color, #ffffff);
            color: var(--text-color, #000000);
        }
        
        /* Tab content styles */
        .tab-content {
            padding: 1rem;
            background: var(--background-color, #ffffff);
            color: var(--text-color, #000000);
        }
        
        /* Heading styles */
        .section-heading {
            color: #3498db !important;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-align: left;
        }
        
        /* Stat counter styles */
        .stat-counter {
            color: #3498db;
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            
        }
        
        /* Category title styles */
        .category-title {
            color: #3498db !important;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-align: left;
        }
        

        /* List styles */
        .list {
            list-style-type: none;
            padding: 0;
        }
        
        /* List item styles */
        .list-item {
            padding: 0.5rem;
            margin-bottom: 0.5rem;
            border-radius: 5px;
            background: var(--background-color, #ffffff);
            color: var(--text-color, #000000);
        }
        </style>
    """, unsafe_allow_html=True)

    # Main score display with improved alignment
    st.markdown(f"""
        <div class="score-card">
            <h1 style='font-size: 72px; margin: 0; line-height: 1.2;'>{analysis['overall_match']}%</h1>
            <p style='font-size: 24px; margin: 10px 0;'>Overall Match</p>
            <div style='display: flex; justify-content: center; gap: 20px; margin-top: 20px;'>
                <div class="metric-card">
                    <h3 style='margin-bottom: 5px;'>Keyword Match</h3>
                    <h2>{analysis['keyword_match_score']}%</h2>
                </div>
                <div class="metric-card">
                    <h3 style='margin-bottom: 5px;'>Achievement Score</h3>
                    <h2>{analysis['impact_scoring']['achievement_metrics']}%</h2>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Category Breakdown with theme-aware colors
    cols = st.columns(4)
    categories = ['technical_skills', 'soft_skills', 'experience', 'education']
    
    for col, category in zip(cols, categories):
        with col:
            cat_name = category.replace('_', ' ').title()
            match = analysis['categories'][category]['match']
            st.markdown(f"""
                <div class="metric-card theme-aware-text" style="background: rgba(52, 152, 219, 0.1);">
                    <h4 class="category-title">{cat_name}</h4>
                    <h2 class="stat-counter">{match}%</h2>
                </div>
            """, unsafe_allow_html=True)

    # Detailed Analysis Sections
    st.markdown('<h3 class="section-heading">📊 Detailed Analysis</h3>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Technical Skills", "Soft Skills", "Experience", "ATS Optimization", "Impact Analysis"])
    
    with tabs[0]:
        st.markdown('<h4 class="category-title">Technical Skills Analysis</h4>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<h5 class="section-heading">Present Skills</h5>', unsafe_allow_html=True)
            for skill in analysis['categories']['technical_skills']['present_skills']:
                st.markdown(f'<div class="list-item">✅ {skill}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<h5 class="section-heading">Missing Skills</h5>', unsafe_allow_html=True)
            for skill in analysis['categories']['technical_skills']['missing_skills']:
                st.markdown(f'<div class="list-item">❌ {skill}</div>', unsafe_allow_html=True)
        
        st.markdown('<h5 class="section-heading">Improvement Suggestions</h5>', unsafe_allow_html=True)
        for suggestion in analysis['categories']['technical_skills']['improvement_suggestions']:
            st.markdown(f"""
                <div class="suggestion-card">
                    💡 {suggestion}
                </div>
            """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("#### Soft Skills Evaluation")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Demonstrated Skills")
            for skill in analysis['categories']['soft_skills']['present_skills']:
                st.markdown(f"✅ {skill}")
        with col2:
            st.markdown("##### Skills to Highlight")
            for skill in analysis['categories']['soft_skills']['missing_skills']:
                st.markdown(f"💭 {skill}")

    with tabs[2]:
        st.markdown("#### Experience Analysis")
        st.markdown("##### Key Strengths")
        for strength in analysis['categories']['experience']['strengths']:
            st.markdown(f"🎯 {strength}")
        
        st.markdown("##### Experience Gaps")
        for gap in analysis['categories']['experience']['gaps']:
            st.markdown(f"🔍 {gap}")

    with tabs[3]:
        st.markdown("#### ATS Optimization")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Formatting Issues")
            for issue in analysis['ats_optimization']['formatting_issues']:
                st.markdown(f"⚠️ {issue}")
        with col2:
            st.markdown("##### Keyword Optimization")
            for suggestion in analysis['ats_optimization']['keyword_optimization']:
                st.markdown(f"🔤 {suggestion}")

    with tabs[4]:
        st.markdown("#### Impact Analysis")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        with metrics_col1:
            st.metric("Achievement Metrics", f"{analysis['impact_scoring']['achievement_metrics']}%")
        with metrics_col2:
            st.metric("Action Verbs Usage", f"{analysis['impact_scoring']['action_verbs']}%")
        with metrics_col3:
            st.metric("Quantifiable Results", f"{analysis['impact_scoring']['quantifiable_results']}%")
        
        st.markdown("##### Impact Improvement Suggestions")
        for suggestion in analysis['impact_scoring']['improvement_suggestions']:
            st.markdown(f"""
                <div class="suggestion-card">
                    📈 {suggestion}
                </div>
            """, unsafe_allow_html=True)

def display_enhancement_suggestions(enhancements):
    if not enhancements:
        st.error("Unable to generate enhancement suggestions")
        return
    
    try:
        st.markdown("### 📝 Resume Enhancement Suggestions")
        
        # Summary Section
        st.subheader("Professional Summary")
        if enhancements.get("summary_section", {}).get("has_summary"):
            st.success("✅ Resume includes a professional summary")
        else:
            st.warning("⚠️ Missing professional summary")
        
        with st.expander("View Summary Suggestions"):
            st.write("#### Suggested Summary")
            st.write(enhancements.get("summary_section", {}).get("sample_summary", "No summary suggestion available"))
            st.write("#### Improvement Points")
            for suggestion in enhancements.get("summary_section", {}).get("suggestions", []):
                st.markdown(f"- {suggestion}")

        # Bullet Points Analysis
        st.subheader("Bullet Points Analysis")
        strength = enhancements.get("bullet_points", {}).get("strength", 0)
        st.metric("Bullet Points Strength", f"{strength}%")
        
        with st.expander("View Bullet Point Improvements"):
            weak_bullets = enhancements.get("bullet_points", {}).get("weak_bullets", [])
            improved_versions = enhancements.get("bullet_points", {}).get("improved_versions", [])
            for weak, improved in zip(weak_bullets, improved_versions):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original:**")
                    st.markdown(f"- {weak}")
                with col2:
                    st.markdown("**Improved:**")
                    st.markdown(f"- {improved}")

        # Power Verbs
        st.subheader("Action Verbs Enhancement")
        with st.expander("View Action Verb Suggestions"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Current Verbs:**")
                for verb in enhancements.get("power_verbs", {}).get("current_verbs", []):
                    st.markdown(f"- {verb}")
            with col2:
                st.markdown("**Suggested Stronger Alternatives:**")
                for verb in enhancements.get("power_verbs", {}).get("suggested_verbs", []):
                    st.markdown(f"- {verb}")

        # Technologies and Certifications
        st.subheader("Technical Profile Enhancement")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Technologies to Add:**")
            for tech in enhancements.get("technologies", {}).get("suggested_additions", []):
                st.markdown(f"- {tech}")
        with col2:
            st.markdown("**Recommended Certifications:**")
            for cert in enhancements.get("certifications", {}).get("relevant_certs", []):
                st.markdown(f"- {cert}")
                
    except Exception as e:
        st.error(f"Error displaying enhancement suggestions: {str(e)}")

def display_linkedin_optimization(linkedin_suggestions):
    if not linkedin_suggestions:
        st.error("Unable to generate LinkedIn optimization suggestions")
        return
    
    try:
        st.markdown("### 💼 LinkedIn Profile Optimization")
        
        # Headline Suggestions
        st.subheader("Professional Headlines")
        for headline in linkedin_suggestions.get("headline_suggestions", []):
            st.markdown(f"- ✨ {headline}")

        # About Section
        st.subheader("About Section")
        st.markdown(linkedin_suggestions.get("about_section", "No about section suggestion available"))

        # Key Achievements
        st.subheader("Key Achievements to Highlight")
        for achievement in linkedin_suggestions.get("key_achievements", []):
            st.markdown(f"- 🏆 {achievement}")

        # Skills
        st.subheader("Recommended Skills")
        for skill in linkedin_suggestions.get("skills_to_add", []):
            st.markdown(f"- 🔧 {skill}")

        # Profile Optimization Tips
        st.subheader("Profile Optimization Tips")
        for tip in linkedin_suggestions.get("profile_optimization", []):
            st.markdown(f"- 💡 {tip}")
            
    except Exception as e:
        st.error(f"Error displaying LinkedIn optimization: {str(e)}")