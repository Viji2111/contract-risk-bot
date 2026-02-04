"""
AI-powered clause explanation using Groq API (FREE & FAST!)
Falls back to templates if API is unavailable
"""
import streamlit as st
from groq import Groq
from risk_explanations import (
    get_template_explanation,
    get_hindi_template_explanation,
)

# ---------------- LOAD API KEY ----------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

AI_AVAILABLE = False
client = None

if GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_"):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        AI_AVAILABLE = True
    except Exception:
        AI_AVAILABLE = False


# ---------------- MAIN FUNCTION ----------------
def explain_clause(clause: str, language: str = "en", risk_type: str = None) -> str:
    """
    Explain contract clause using Groq AI.
    Falls back to templates if AI unavailable.
    """

    # 🔁 Fallback if AI unavailable
    if not AI_AVAILABLE or not client:
        if language == "hi":
            return (
                get_hindi_template_explanation(risk_type)
                if risk_type
                else "⚠️ AI अभी उपलब्ध नहीं है।"
            )
        return (
            get_template_explanation(risk_type)
            if risk_type
            else "⚠️ AI explanation unavailable."
        )

    # 🌍 Language instruction
    if language == "hi":
        lang_instruction = "Explain only in simple Hindi."
    elif language == "both":
        lang_instruction = "Explain in English first, then Hindi."
    else:
        lang_instruction = "Explain in simple business English."

    prompt = f"""
{lang_instruction}

Explain the contract clause WITHOUT repeating it.

Provide exactly these sections:
1. Meaning
2. Risk
3. Who Benefits
4. Risk Mitigation (clear actions)

Keep it practical and short.

Clause:
{clause}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ FAST + FREE
            messages=[
                {"role": "system", "content": "You are a legal risk advisor for non-lawyers."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=350,
        )

        return response.choices[0].message.content.strip()

    except Exception:
        if language == "hi":
            return "⚠️ AI अस्थायी रूप से व्यस्त है।"
        return "⚠️ AI service is temporarily busy."



def explain_multiple_risks(clause: str, risks: list, language: str = "en") -> str:
    """
    Explain a clause with multiple risks using Groq
    """
    if not AI_AVAILABLE or not client:
        explanations = []
        for risk in risks[:2]:
            if language == "hi":
                explanations.append(get_hindi_template_explanation(risk))
            else:
                explanations.append(get_template_explanation(risk))
        return "\n\n---\n\n".join(explanations)
    
    risk_list = ", ".join(risks)
    
    if language == "hi":
        lang_instruction = "Explain in Hindi (हिंदी में समझाएं)."
    else:
        lang_instruction = "Explain in English."
    
    prompt = f"""{lang_instruction}

This contract clause has multiple risk factors: {risk_list}

Provide a comprehensive explanation covering:
1. **Overall Meaning** - What this clause does
2. **Combined Risks** - How these risks work together
3. **Who Benefits** - Which party is protected
4. **Recommendation** - Best course of action

Clause:
{clause}"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful legal assistant that explains contract clauses in simple, practical language."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=700
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Groq API Error: {str(e)}")
        explanations = []
        for risk in risks[:2]:
            if language == "hi":
                explanations.append(get_hindi_template_explanation(risk))
            else:
                explanations.append(get_template_explanation(risk))
        
        return "\n\n---\n\n".join(explanations)


def test_groq_connection() -> bool:
    """
    Test if Groq API is working
    Returns True if connected, False otherwise
    """
    if not client:
        return False
        
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": "Say 'OK'"}],
            model="llama-3.1-8b-instant",
            max_tokens=10
        )
        return True
    except Exception as e:
        print(f"Groq connection test failed: {e}")
        return False