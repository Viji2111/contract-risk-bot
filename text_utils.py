"""
Text extraction and clause splitting utilities
"""
import re
from pypdf import PdfReader


def extract_text(uploaded_file):
    """
    Extract text from PDF or TXT file
    Supports Unicode (Hindi/English)
    """
    try:
        if uploaded_file.type == "application/pdf":
            pdf = PdfReader(uploaded_file)
            text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
        else:
            # TXT file
            text = uploaded_file.read().decode("utf-8", errors='ignore')
            return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"


def split_clauses(text: str) -> list:
    """
    Split contract into individual clauses
    Works for both English and Hindi
    """
    # Common clause markers
    patterns = [
        r'\n\d+\.\s+',           # 1. 2. 3.
        r'\n\d+\)\s+',           # 1) 2) 3)
        r'\n[A-Z]\.\s+',         # A. B. C.
        r'\n[A-Z]\)\s+',         # A) B) C)
        r'\nSection\s+\d+',      # Section 1, Section 2
        r'\nArticle\s+\d+',      # Article 1, Article 2
        r'\nClause\s+\d+',       # Clause 1, Clause 2
        r'\n[क-ह]\.\s+',         # Hindi: क. ख. ग.
        r'\nधारा\s+\d+',         # Hindi: धारा 1, धारा 2
        r'\nअनुच्छेद\s+\d+',    # Hindi: अनुच्छेद
    ]
    
    # Combine all patterns
    combined_pattern = '|'.join(patterns)
    
    # Split text
    clauses = re.split(combined_pattern, text)
    
    # Clean and filter
    cleaned_clauses = []
    for clause in clauses:
        clause = clause.strip()
        # Keep clauses that are substantial (>50 chars)
        if len(clause) > 50:
            cleaned_clauses.append(clause)
    
    # If no clauses found, split by double newlines
    if len(cleaned_clauses) < 2:
        paragraphs = text.split('\n\n')
        cleaned_clauses = [p.strip() for p in paragraphs if len(p.strip()) > 50]
    
    return cleaned_clauses


def clean_text(text: str) -> str:
    """Remove extra whitespace and normalize text"""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove multiple newlines
    text = re.sub(r'\n+', '\n', text)
    return text.strip()