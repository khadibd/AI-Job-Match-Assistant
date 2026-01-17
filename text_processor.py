# %%writefile ai-job-assistant/utils/text_processor.py
"""
Text processing utilities
Simple and reliable for Jupyter
"""
import re
from typing import List, Dict, Any

class TextProcessor:
    def __init__(self):
        print("✅ TextProcessor initialized")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Lowercase
        text = text.lower()
        
        # Remove special characters but keep basic ones
        text = re.sub(r'[^\w\s.,\-@+#]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills using keyword matching"""
        # Common AI/ML skills dictionary
        skill_patterns = {
            'python': r'\bpython\b',
            'tensorflow': r'\btensorflow\b|\btf\b',
            'pytorch': r'\bpytorch\b|\btorch\b',
            'keras': r'\bkeras\b',
            'machine learning': r'\bmachine learning\b|\bml\b',
            'deep learning': r'\bdeep learning\b',
            'nlp': r'\bnlp\b|\bnatural language processing\b',
            'computer vision': r'\bcomputer vision\b|\bcv\b|\bopencv\b',
            'aws': r'\baws\b|\bamazon web services\b',
            'docker': r'\bdocker\b',
            'kubernetes': r'\bkubernetes\b|\bk8s\b',
            'sql': r'\bsql\b',
            'git': r'\bgit\b|\bgithub\b|\bgitlab\b',
            'linux': r'\blinux\b',
            'pandas': r'\bpandas\b',
            'numpy': r'\bnumpy\b',
            'scikit-learn': r'\bscikit-learn\b|\bsklearn\b',
            'matplotlib': r'\bmatplotlib\b',
            'seaborn': r'\bseaborn\b',
            'fastapi': r'\bfastapi\b',
            'streamlit': r'\bstreamlit\b',
            'spark': r'\bspark\b|\bpyspark\b',
        }
        
        text_lower = self.clean_text(text)
        found_skills = []
        
        for skill, pattern in skill_patterns.items():
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return list(set(found_skills))
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience information"""
        text_lower = self.clean_text(text)
        
        # Look for years of experience
        years_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience',
            r'experience.*?(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)\s*(?:of)?\s*experience',
        ]
        
        experience_years = 0
        
        for pattern in years_patterns:
            matches = re.search(pattern, text_lower)
            if matches:
                groups = matches.groups()
                if len(groups) == 2:
                    # Range like "3-5 years"
                    try:
                        min_years = int(groups[0])
                        max_years = int(groups[1])
                        experience_years = (min_years + max_years) / 2
                    except:
                        experience_years = 0
                elif len(groups) == 1:
                    try:
                        experience_years = int(groups[0])
                    except:
                        experience_years = 0
                break
        
        # Check for management keywords
        management_keywords = ['lead', 'manager', 'director', 'head', 'supervisor', 'team lead']
        has_management = any(keyword in text_lower for keyword in management_keywords)
        
        # Education level
        education_keywords = {
            'phd': ['phd', 'ph.d', 'doctorate'],
            'masters': ['masters', 'ms', 'm.sc', 'm.eng'],
            'bachelors': ['bachelor', 'bs', 'b.sc', 'b.eng', 'ba']
        }
        
        education = 'unknown'
        for level, keywords in education_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                education = level
                break
        
        return {
            'years': float(experience_years),
            'has_management': has_management,
            'education': education
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Complete text analysis"""
        clean_text = self.clean_text(text)
        
        return {
            'skills': self.extract_skills(clean_text),
            'experience': self.extract_experience(clean_text),
            'word_count': len(clean_text.split()),
            'char_count': len(clean_text)
        }

# Test function
def test_processor():
    """Test the text processor"""
    print("🧪 Testing TextProcessor...")
    
    processor = TextProcessor()
    
    test_resume = """
    John Doe
    AI Engineer with 4 years of experience
    
    SKILLS:
    - Python, TensorFlow, PyTorch
    - AWS, Docker, Kubernetes
    - Machine Learning, Deep Learning
    
    EXPERIENCE:
    - Senior AI Engineer (3 years)
    - Machine Learning Engineer (1 year)
    
    EDUCATION:
    Masters in Computer Science
    """
    
    result = processor.analyze_text(test_resume)
    
    print(f"✅ Skills found: {result['skills']}")
    print(f"✅ Experience: {result['experience']['years']} years")
    print(f"✅ Management: {result['experience']['has_management']}")
    print(f"✅ Education: {result['experience']['education']}")

if __name__ == "__main__":
    test_processor()