import re
from collections import Counter
import spacy
import subprocess

def get_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower()

def extract_keywords(text):
    nlp = get_nlp()  # 👈 Load spaCy model here when needed
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    return Counter(keywords)

def compare_resume_to_jd(resume_text, jd_text):
    resume_keywords = extract_keywords(clean_text(resume_text))
    jd_keywords = extract_keywords(clean_text(jd_text))

    jd_set = set(jd_keywords.keys())
    resume_set = set(resume_keywords.keys())

    matched = jd_set.intersection(resume_set)
    missing = jd_set.difference(resume_set)

    match_score = len(matched) / len(jd_set) if jd_set else 0

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
        "match_score": round(match_score, 2)
    }
