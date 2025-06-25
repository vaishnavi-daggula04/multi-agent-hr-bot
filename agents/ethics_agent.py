# agents/ethics_agent.py

import re
import gender_guesser.detector as gender

detector = gender.Detector()

def infer_gender(name):
    first_name = name.split()[0]
    return detector.get_gender(first_name)

def detect_gap_years(text):
    years = re.findall(r'(20\d{2}|19\d{2})', text)
    years = sorted(set(int(year) for year in years))
    gaps = [y2 - y1 for y1, y2 in zip(years, years[1:])]
    return any(gap > 1 for gap in gaps)

def ethics_check(name, resume_text):
    gender_result = infer_gender(name)
    gap_year_flag = detect_gap_years(resume_text)
    
    fairness_score = 1.0
    if gender_result not in ["unknown", "andy"]:  # i.e., gender could be inferred
        fairness_score -= 0.1
    if gap_year_flag:
        fairness_score -= 0.1

    return {
        "inferred_gender": gender_result,
        "gap_year_flagged": gap_year_flag,
        "fairness_score": round(fairness_score, 2),
        "ethics_flags": {
            "gender_bias_possible": gender_result != "unknown",
            "gap_year_detected": gap_year_flag
        }
    }
