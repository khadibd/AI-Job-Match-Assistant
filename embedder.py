
"""
Simple ML Pipeline for Testing
"""
import numpy as np

class TextProcessor:
    def __init__(self):
        pass
    
    def clean_text(self, text):
        return text.lower() if text else ""
    
    def extract_skills(self, text):
        skills = []
        text_lower = text.lower()
        
        skill_list = ["python", "tensorflow", "pytorch", "aws", "docker", 
                     "machine learning", "sql", "react", "javascript"]
        
        for skill in skill_list:
            if skill in text_lower:
                skills.append(skill)
        
        return skills
    
    def extract_experience(self, text):
        import re
        years = 0
        match = re.search(r'(\d+)\s*(?:years?|yrs?)', text.lower())
        if match:
            try:
                years = int(match.group(1))
            except:
                pass
        
        return {"years": years, "has_management": False, "education": "unknown"}

class SimilarityMatcher:
    def __init__(self, model_name="TF-IDF"):
        self.model_name = model_name
    
    def get_embeddings(self, texts):
        return np.random.rand(len(texts), 10)

class ResumeEmbedder:
    def __init__(self, model_name="TF-IDF"):
        self.processor = TextProcessor()
        self.matcher = SimilarityMatcher(model_name)
        print(f"ResumeEmbedder initialized with {model_name}")
    
    def process_resume(self, text, resume_id=None, metadata=None):
        skills = self.processor.extract_skills(text)
        experience = self.processor.extract_experience(text)
        
        return {
            "id": resume_id or "resume_1",
            "skills": skills,
            "experience_years": experience["years"],
            "embedding": [0.1] * 10,
            "metadata": metadata or {}
        }
    
    def process_job_description(self, text, job_id=None, metadata=None):
        required_skills = self.processor.extract_skills(text)
        experience_needed = self.processor.extract_experience(text)
        
        return {
            "id": job_id or "job_1",
            "required_skills": required_skills,
            "experience_needed": experience_needed["years"],
            "embedding": [0.2] * 10,
            "metadata": metadata or {}
        }
    
    def find_best_matches(self, resume_data, jobs_data, top_k=5):
        results = []
        
        for job in jobs_data:
            # Simple matching logic
            matched_skills = set(resume_data["skills"]) & set(job["required_skills"])
            total_skills = len(job["required_skills"])
            match_ratio = len(matched_skills) / max(total_skills, 1)
            
            score = match_ratio * 100
            
            results.append({
                "job_title": job["metadata"].get("title", "Unknown"),
                "company": job["metadata"].get("company", "Unknown"),
                "match_percentage": round(score, 1),
                "matched_skills": list(matched_skills),
                "missing_skills": list(set(job["required_skills"]) - set(resume_data["skills"])),
                "total_matched": len(matched_skills),
                "total_required": total_skills
            })
        
        results.sort(key=lambda x: x["match_percentage"], reverse=True)
        return results[:top_k]

# For backward compatibility
process_job = process_job_description
match_resume_to_jobs = find_best_matches
