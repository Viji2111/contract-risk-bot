"""
AI-powered clause explanation using Groq API (FREE & FAST!)
Falls back to templates if API is unavailable
"""
import os
import streamlit as st
from groq import Groq
from risk_explanations import get_template_explanation, get_hindi_template_explanation


# Get from environment (Streamlit secrets automatically go into os.environ)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY or not GROQ_API_KEY.startswith('gsk_'):
    st.error("❌ No valid GROQ_API_KEY in secrets!")
    st.stop()

# Cache client init to avoid recreating on every rerun
@st.cache_resource
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)

client = get_groq_client()

# Test connection once (optional, in sidebar or expander)
with st.expander("API Status"):
    try:
        test_response = client.chat.completions.create(
            messages=[{"role": "user", "content": "test"}],
            model="llama-3.1-8b-instant",
            max_tokens=1
        )
        st.success("✅ Groq API connected!")
    except Exception as e:
        st.error(f"❌ API error: {str(e)}")


def explain_clause(clause: str, language: str = "en", risk_type: str = None) -> str:
    """
    Get AI-powered explanation of a contract clause using Groq
    
    Args:
        clause: The contract clause text
        language: 'en' for English, 'hi' for Hindi, 'both' for bilingual
        risk_type: Optional risk type for better fallback
    
    Returns:
        Formatted explanation
    """    
    # If AI is not available, use templates
    if not AI_AVAILABLE or not client:
        print("⚠️ Using template fallback")
        if language == "hi":
            return get_hindi_template_explanation(risk_type) if risk_type else "AI अनुपलब्ध है।"
        return get_template_explanation(risk_type) if risk_type else "AI unavailable."
    
    # Prepare language-specific instructions
    if language == "hi":
        lang_instruction = "Explain in Hindi (हिंदी में समझाएं). Use simple Hindi that common people can understand."
    elif language == "both":
        lang_instruction = "Provide explanation in both English and Hindi side by side."
    else:
        lang_instruction = "Explain in clear, simple English."
    
    # Create prompt
    prompt = f"""{lang_instruction}

Analyze this contract clause and provide a practical explanation with these 4 sections:

1. **Meaning** - What this clause says in everyday language
2. **Risk** - What problems or costs this could cause for the person signing
3. **Who Benefits** - Which party gains advantage from this clause
4. **Recommendation** - Specific action to take (negotiate, remove, modify, or accept)

Contract Clause:
{clause}

Keep each section concise (2-3 sentences max). Be direct and practical."""

    try:
        print("🚀 Calling Groq API...")
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful legal assistant that explains contract clauses in simple, practical language. You focus on real-world implications and actionable advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=600
        )
        
        explanation = chat_completion.choices[0].message.content
        print("✅ Got AI response successfully!")
        return explanation
        
    except Exception as e:
        print(f"❌ Groq API Error during explanation: {str(e)}")
        # Fallback to templates
        if language == "hi":
            return get_hindi_template_explanation(risk_type) if risk_type else "⚠️ AI अस्थायी रूप से अनुपलब्ध है।"
        return get_template_explanation(risk_type) if risk_type else "⚠️ AI temporarily unavailable."


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