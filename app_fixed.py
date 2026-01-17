# %%writefile frontend/app_fixed.py
"""
FIXED Streamlit App with Correct Imports
"""
import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import sys

# ============================================
# CRITICAL: ADD CURRENT DIRECTORY TO PYTHON PATH
# ============================================
current_dir = os.getcwd()
sys.path.insert(0, current_dir)  # Add current directory
sys.path.insert(0, os.path.join(current_dir, ".."))  # Add parent

print(f"📍 Python path: {sys.path[:3]}")

# ============================================
# INITIALIZE SESSION STATE
# ============================================
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""

if 'jobs' not in st.session_state:
    st.session_state.jobs = []

if 'matches' not in st.session_state:
    st.session_state.matches = []

# ============================================
# SIMULATED ML MODULES (For testing)
# ============================================
class SimpleTextProcessor:
    def __init__(self):
        pass
    
    def clean_text(self, text):
        return text.lower() if text else ""
    
    def extract_skills(self, text):
        skills = []
        text_lower = text.lower()
        skill_keywords = {
            'python': ['python'],
            'tensorflow': ['tensorflow', 'tf'],
            'pytorch': ['pytorch'],
            'aws': ['aws', 'amazon web services'],
            'docker': ['docker'],
            'machine learning': ['machine learning', 'ml'],
            'sql': ['sql'],
            'react': ['react', 'react.js'],
            'javascript': ['javascript', 'js']
        }
        
        for skill, keywords in skill_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    skills.append(skill)
                    break
        
        return list(set(skills))
    
    def extract_experience(self, text):
        import re
        text_lower = text.lower()
        
        # Find years
        years = 0
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience',
            r'experience.*?(\d+)\+?\s*(?:years?|yrs?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    years = int(match.group(1))
                    break
                except:
                    pass
        
        return {'years': years, 'has_management': False, 'education': 'unknown'}

class SimpleSimilarityMatcher:
    def __init__(self, model_name="simple"):
        self.model_name = model_name
    
    def get_embeddings(self, texts):
        # Simple random embeddings for testing
        import numpy as np
        return np.random.rand(len(texts), 10)

class SimpleResumeEmbedder:
    def __init__(self, model_name="simple"):
        self.processor = SimpleTextProcessor()
        self.matcher = SimpleSimilarityMatcher(model_name)
        print(f"✅ Using SimpleResumeEmbedder ({model_name})")
    
    def process_resume(self, text, resume_id=None, metadata=None):
        skills = self.processor.extract_skills(text)
        experience = self.processor.extract_experience(text)
        
        return {
            'id': resume_id or 'resume_1',
            'skills': skills,
            'experience_years': experience['years'],
            'has_management': experience['has_management'],
            'education': experience['education'],
            'embedding': [0.1, 0.2, 0.3],  # dummy embedding
            'metadata': metadata or {}
        }
    
    def process_job(self, text, job_id=None, metadata=None):
        required_skills = self.processor.extract_skills(text)
        experience_needed = self.processor.extract_experience(text)
        
        return {
            'id': job_id or 'job_1',
            'required_skills': required_skills,
            'experience_needed': experience_needed['years'],
            'requires_management': experience_needed['has_management'],
            'education_required': experience_needed['education'],
            'embedding': [0.4, 0.5, 0.6],  # dummy embedding
            'metadata': metadata or {}
        }
    
    def match_resume_to_jobs(self, resume_data, jobs_data, top_k=5):
        results = []
        
        for job in jobs_data:
            # Calculate skill match
            resume_skills = set(resume_data.get('skills', []))
            job_skills = set(job.get('required_skills', []))
            
            skill_overlap = len(resume_skills.intersection(job_skills))
            total_required = len(job_skills)
            skill_match = skill_overlap / max(total_required, 1)
            
            # Experience match
            resume_exp = resume_data.get('experience_years', 0)
            job_exp = job.get('experience_needed', 0)
            
            if job_exp <= 0:
                exp_match = 1.0
            elif resume_exp >= job_exp:
                exp_match = 1.0
            else:
                exp_match = resume_exp / max(job_exp, 1)
            
            # Combined score
            combined_score = 0.6 * skill_match + 0.4 * exp_match
            
            # Match level
            if combined_score >= 0.8:
                match_level = "🔥 Excellent"
            elif combined_score >= 0.6:
                match_level = "👍 Good"
            elif combined_score >= 0.4:
                match_level = "⚠️ Fair"
            else:
                match_level = "❌ Poor"
            
            result = {
                'job_title': job['metadata'].get('title', 'Unknown'),
                'company': job['metadata'].get('company', 'Unknown'),
                'match_percentage': round(combined_score * 100, 1),
                'match_level': match_level,
                'matched_skills': list(resume_skills.intersection(job_skills)),
                'missing_skills': list(job_skills - resume_skills),
                'total_skills_matched': skill_overlap,
                'total_skills_required': total_required,
                'skill_match': round(skill_match, 2),
                'experience_match': round(exp_match, 2)
            }
            
            results.append(result)
        
        # Sort by score
        results.sort(key=lambda x: x['match_percentage'], reverse=True)
        return results[:top_k]

# ============================================
# PAGE SETUP
# ============================================
st.set_page_config(
    page_title="AI Job Match Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-title { text-align: center; color: #1E3A8A; font-size: 2.5rem; }
    .match-card { background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 5px solid #3B82F6; }
    .skill-tag { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 0.2rem 0.6rem; margin: 0.2rem; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">🤖 AI Job Match Assistant</h1>', unsafe_allow_html=True)
st.markdown("### Test Version - Working Demo")

# Sample Data
SAMPLE_RESUME = """AI Engineer with 3 years experience in Python and TensorFlow.
Skills: Python, Machine Learning, AWS, Docker.
Built ML models for computer vision projects.
Education: Masters in Computer Science."""

SAMPLE_JOBS = [
    {
        "title": "Machine Learning Engineer",
        "company": "TechCorp",
        "description": "Looking for ML Engineer with Python and TensorFlow. AWS experience required.",
        "skills": ["python", "tensorflow", "aws", "machine learning"]
    },
    {
        "title": "Frontend Developer",
        "company": "WebDev Inc",
        "description": "React developer with JavaScript experience. 2+ years required.",
        "skills": ["react", "javascript", "css", "html"]
    }
]

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    top_k = st.slider("Results to show", 1, 10, 5)
    
    if st.button("Load Sample Data"):
        st.session_state.resume_text = SAMPLE_RESUME
        st.session_state.jobs = SAMPLE_JOBS.copy()
        st.success("Sample data loaded!")
    
    if st.button("Clear All"):
        st.session_state.resume_text = ""
        st.session_state.jobs = []
        st.session_state.matches = []
        st.success("Data cleared")

# Main Interface
col1, col2 = st.columns(2)

with col1:
    st.header("📝 Your Resume")
    resume_text = st.text_area(
        "Enter resume:",
        height=250,
        value=st.session_state.resume_text,
        key="resume_input"
    )
    if resume_text != st.session_state.resume_text:
        st.session_state.resume_text = resume_text

with col2:
    st.header("📋 Job Descriptions")
    
    with st.expander("➕ Add Job"):
        title = st.text_input("Job Title", key="job_title")
        company = st.text_input("Company", key="company")
        desc = st.text_area("Description", height=150, key="desc")
        
        if st.button("Add Job", key="add_job"):
            if desc:
                st.session_state.jobs.append({
                    "title": title or "Untitled",
                    "company": company or "Unknown",
                    "description": desc,
                    "skills": []
                })
                st.success("Job added!")
                st.rerun()
    
    if st.session_state.jobs:
        st.write(f"Jobs loaded: {len(st.session_state.jobs)}")

# Process Button
if st.button("🎯 Find Matches", type="primary"):
    if not st.session_state.resume_text.strip():
        st.error("Please enter resume text")
    elif not st.session_state.jobs:
        st.error("Please add jobs")
    else:
        with st.spinner("Analyzing..."):
            try:
                # Try to import real modules first
                try:
                    from ml_pipeline.embedder import ResumeEmbedder
                    embedder = ResumeEmbedder()
                    st.success("✅ Using real ML pipeline")
                except ImportError:
                    # Use simulated version
                    embedder = SimpleResumeEmbedder()
                    st.info("⚠️ Using simulated matching (real modules not found)")
                
                # Process resume
                resume_data = embedder.process_resume(
                    st.session_state.resume_text,
                    metadata={"source": "web_app"}
                )
                
                # Process jobs
                jobs_data = []
                for job in st.session_state.jobs:
                    job_data = embedder.process_job(
                        job['description'],
                        metadata=job
                    )
                    jobs_data.append(job_data)
                
                # Get matches
                matches = embedder.match_resume_to_jobs(resume_data, jobs_data, top_k)
                st.session_state.matches = matches
                
                if matches:
                    st.success(f"✅ Found {len(matches)} matches!")
                else:
                    st.info("No matches found")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Show Results
if st.session_state.matches:
    st.header("🎯 Results")
    
    for match in st.session_state.matches:
        with st.container():
            st.markdown('<div class="match-card">', unsafe_allow_html=True)
            
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.subheader(f"{match['job_title']}")
                st.write(f"Company: {match['company']}")
            with col_b:
                st.metric("Match", f"{match['match_percentage']}%")
            
            st.write(f"**Level:** {match['match_level']}")
            
            if match['matched_skills']:
                st.write("✅ Matched Skills:")
                for skill in match['matched_skills'][:5]:
                    st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Export
    if st.session_state.matches:
        df = pd.DataFrame(st.session_state.matches)
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            "matches.csv",
            "text/csv"
        )

# Footer
st.markdown("---")
st.markdown("*AI Job Match Assistant - Demo Version*")