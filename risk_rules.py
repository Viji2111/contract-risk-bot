"""
Risk detection patterns and rules
"""
import re
from language_utils import detect_language, translate_text


# Risk patterns for both English and Hindi
RISK_PATTERNS = {
    "Liability Cap": [
        r"liability.*limited\s+to",
        r"maximum\s+liability",
        r"shall\s+not\s+exceed",
        r"liability.*capped",
        r"दायित्व.*सीमित",
        r"अधिकतम\s+दायित्व",
    ],
    
    "Indemnification": [
        r"indemnify",
        r"hold\s+harmless",
        r"defend.*against",
        r"indemnification",
        r"क्षतिपूर्ति",
        r"हानि\s+रहित",
        r"मुआवजा",
    ],
    
    "Automatic Renewal": [
        r"automatically\s+renew",
        r"auto-?renew",
        r"shall\s+renew\s+unless",
        r"perpetual\s+renewal",
        r"स्वचालित.*नवीनीकरण",
        r"स्वतः.*नवीकरण",
    ],
    
    "Termination Fee": [
        r"termination\s+fee",
        r"early\s+termination.*penalty",
        r"cancellation\s+charge",
        r"exit\s+fee",
        r"समाप्ति\s+शुल्क",
        r"जुर्माना",
        r"रद्दीकरण\s+शुल्क",
    ],
    
    "IP Transfer": [
        r"intellectual\s+property.*transfer",
        r"ownership.*work\s+product",
        r"all\s+rights.*assigned",
        r"IP.*belongs\s+to",
        r"बौद्धिक\s+संपदा.*हस्तांतरण",
        r"स्वामित्व.*हस्तांतरित",
    ],
    
    "Non-Compete": [
        r"non-?compete",
        r"shall\s+not.*compet",
        r"restrictive\s+covenant",
        r"non-?solicitation",
        r"प्रतिस्पर्धा.*नहीं",
        r"प्रतिबंधात्मक",
    ],
    
    "Arbitration Clause": [
        r"mandatory\s+arbitration",
        r"binding\s+arbitration",
        r"arbitration.*exclusive\s+remedy",
        r"waive.*right.*jury",
        r"अनिवार्य\s+मध्यस्थता",
        r"बाध्यकारी\s+मध्यस्थता",
    ],
    
    "Unilateral Changes": [
        r"modify.*at\s+any\s+time",
        r"change.*without\s+notice",
        r"reserve.*right.*modify",
        r"sole\s+discretion",
        r"बिना\s+सूचना.*बदल",
        r"किसी\s+भी\s+समय.*संशोधन",
    ],
    
    "Limited Warranty": [
        r"as\s+is",
        r"no\s+warranty",
        r"warranty\s+disclaim",
        r"without\s+warranty.*kind",
        r"कोई\s+वारंटी\s+नहीं",
        r"जैसा\s+है",
    ],
    
    "Data Rights": [
        r"data.*belong.*to",
        r"unlimited.*data\s+rights",
        r"perpetual.*data\s+license",
        r"use.*data.*any\s+purpose",
        r"डेटा.*अधिकार",
        r"असीमित.*उपयोग",
    ],
    
    "Jurisdiction": [
        r"exclusive\s+jurisdiction",
        r"courts?\s+of.*shall\s+have\s+jurisdiction",
        r"forum.*venue",
        r"अनन्य\s+क्षेत्राधिकार",
    ],
    
    "Confidentiality Burden": [
        r"confidential.*perpetuity",
        r"confidential.*indefinitely",
        r"गोपनीय.*हमेशा",
    ],
    
    "Payment Terms": [
        r"non-?refundable",
        r"payment.*advance",
        r"no\s+refund",
        r"वापसी\s+नहीं",
        r"अग्रिम\s+भुगतान",
    ],
    
    "Force Majeure Abuse": [
        r"force\s+majeure.*broadly",
        r"suspend.*force\s+majeure",
        r"अप्रत्याशित\s+घटना",
    ],
    
    "Assignment Rights": [
        r"may\s+assign.*without\s+consent",
        r"freely\s+assign",
        r"सहमति\s+के\s+बिना.*हस्तांतरण",
    ],
}


# Risk severity levels
RISK_LEVELS = {
    "Liability Cap": "High",
    "Indemnification": "High",
    "IP Transfer": "High",
    "Data Rights": "High",
    "Non-Compete": "Medium",
    "Automatic Renewal": "Medium",
    "Termination Fee": "Medium",
    "Unilateral Changes": "Medium",
    "Payment Terms": "Medium",
    "Arbitration Clause": "Low",
    "Limited Warranty": "Low",
    "Jurisdiction": "Low",
    "Confidentiality Burden": "Medium",
    "Force Majeure Abuse": "Low",
    "Assignment Rights": "Medium",
}


def detect_risks(clause: str) -> list:
    """
    Detect risks in a contract clause
    Works for both English and Hindi text
    
    Args:
        clause: Contract clause text
    
    Returns:
        List of detected risk types
    """
    if not clause or len(clause.strip()) < 20:
        return []
    
    risks = []
    clause_lower = clause.lower()
    
    # Get language
    lang = detect_language(clause)
    
    # For Hindi/mixed, also check translated version
    clauses_to_check = [clause_lower]
    if lang in ["hi", "mixed"]:
        try:
            translated = translate_text(clause, "en").lower()
            clauses_to_check.append(translated)
        except:
            pass
    
    # Check each risk pattern
    for risk_type, patterns in RISK_PATTERNS.items():
        found = False
        for test_clause in clauses_to_check:
            for pattern in patterns:
                if re.search(pattern, test_clause, re.IGNORECASE):
                    risks.append(risk_type)
                    found = True
                    break
            if found:
                break
    
    # Remove duplicates while preserving order
    seen = set()
    unique_risks = []
    for risk in risks:
        if risk not in seen:
            seen.add(risk)
            unique_risks.append(risk)
    
    return unique_risks


def get_risk_severity(risk_type: str) -> str:
    """Get severity level for a risk type"""
    return RISK_LEVELS.get(risk_type, "Medium")


def calculate_risk_score(clauses: list) -> dict:
    """
    Calculate overall risk score for contract
    
    Returns:
        Dictionary with score, grade, and statistics
    """
    if not clauses:
        return {
            "score": 100,
            "grade": "A+",
            "total_clauses": 0,
            "risky_clauses": 0,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0,
        }
    
    total_risks = 0
    high_risks = 0
    medium_risks = 0
    low_risks = 0
    risky_clause_count = 0
    
    for clause in clauses:
        risks = detect_risks(clause)
        if risks:
            risky_clause_count += 1
            total_risks += len(risks)
            
            for risk in risks:
                level = get_risk_severity(risk)
                if level == "High":
                    high_risks += 1
                elif level == "Medium":
                    medium_risks += 1
                else:
                    low_risks += 1
    
    # Calculate score (0-100)
    # Penalize based on risk density and severity
    risk_density = total_risks / len(clauses) if len(clauses) > 0 else 0
    
    score = 100
    score -= (risk_density * 25)  # General risk penalty
    score -= (high_risks * 8)     # High risk penalty
    score -= (medium_risks * 4)   # Medium risk penalty
    score -= (low_risks * 2)      # Low risk penalty
    
    score = max(0, min(100, score))  # Clamp between 0-100
    
    # Determine grade
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"
    
    return {
        "score": round(score, 1),
        "grade": grade,
        "total_clauses": len(clauses),
        "risky_clauses": risky_clause_count,
        "high_risk_count": high_risks,
        "medium_risk_count": medium_risks,
        "low_risk_count": low_risks,
    }