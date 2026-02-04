"""
Contract Risk Assessment Bot
Streamlit Application with AI + Hindi Support
"""
import streamlit as st
import io
from datetime import datetime

from text_utils import extract_text, split_clauses
from risk_rules import detect_risks, get_risk_severity, calculate_risk_score
from ai_explainer import explain_clause, explain_multiple_risks
from language_utils import detect_language, get_language_display_name, is_hindi_text


# Page configuration
st.set_page_config(
    page_title="Contract Guardian AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    .risk-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 1rem 0;
        transition: transform 0.2s;
    }
    
    .risk-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    
    .high-risk {
        border-left: 6px solid #f44336;
    }
    
    .medium-risk {
        border-left: 6px solid #ff9800;
    }
    
    .low-risk {
        border-left: 6px solid #4caf50;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .stat-box h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .stat-box p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        color: #666;
        font-weight: 600;
    }
    
    .info-banner {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .warning-banner {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    
    .success-banner {
        background: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .stExpander {
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)


# Hero Section
st.markdown("""
<div class="main-header">
    <h1>🛡️ Contract Guardian AI</h1>
    <p>Protect yourself from risky contract clauses • English & Hindi Support • Powered by AI</p>
</div>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Language selection
    output_lang_option = st.selectbox(
        "🌐 Explanation Language",
        ["🇬🇧 English", "🇮🇳 Hindi (हिंदी)", "🌍 Both Languages"],
        help="Choose the language for AI explanations"
    )
    
    lang_map = {
        "🇬🇧 English": "en",
        "🇮🇳 Hindi (हिंदी)": "hi",
        "🌍 Both Languages": "both"
    }
    output_lang = lang_map[output_lang_option]
    
    st.markdown("---")
    
    # Info section
    st.markdown("### 📚 About")
    st.info("""
    This tool analyzes contracts to identify potentially risky clauses and provides simple explanations.
    
    **Features:**
    - 15+ risk pattern detection
    - AI-powered explanations
    - Bilingual support (English/Hindi)
    - Risk scoring (0-100)
    - Downloadable reports
    """)
    
    st.markdown("---")
    if st.button("🔌 Test API Connection"):
        from ai_explainer import test_groq_connection
    
        with st.spinner("Testing Groq API..."):
            if test_groq_connection():
                st.success("✅ Groq API Connected!")
            else:
                st.error("❌ API connection failed. Using template explanations.")
    
    # Sample contracts
    st.markdown("### 📄 Try Sample Contracts")
    if st.button("Load English Sample", use_container_width=True):
        st.session_state['use_sample'] = 'english'
    if st.button("Load Hindi Sample", use_container_width=True):
        st.session_state['use_sample'] = 'hindi'


# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📤 Upload Contract")

with col2:
    st.markdown("### 🎯 Quick Stats")


# File uploader
uploaded_file = st.file_uploader(
    "Upload your contract document (PDF or TXT)",
    type=["pdf", "txt"],
    help="Maximum file size: 10MB"
)


# Handle sample contracts
if 'use_sample' in st.session_state:
    sample_type = st.session_state['use_sample']
    
    if sample_type == 'english':
        sample_text = """
SERVICE AGREEMENT

1. Liability Limitation
The Company's total liability under this Agreement shall be limited to the amount paid by Client in the preceding 12 months, regardless of the nature or cause of action.

2. Indemnification Clause
Client agrees to indemnify, defend, and hold harmless the Company from any claims, damages, or expenses arising from Client's use of the services.

3. Automatic Renewal
This Agreement shall automatically renew for successive one-year terms unless Client provides written notice of non-renewal at least 90 days prior to the end of the current term.

4. Intellectual Property Assignment
All work product, deliverables, and intellectual property created during the term of this Agreement shall be the exclusive property of the Company.

5. Non-Compete Provision
Client agrees not to engage in any business that competes with Company's services for a period of 2 years following termination of this Agreement.

6. Payment Terms
All payments are non-refundable. Client shall pay the full annual fee in advance within 15 days of invoice date.

7. Modification Rights
Company reserves the right to modify the terms of this Agreement at any time at its sole discretion without prior notice to Client.

8. Arbitration
Any dispute arising under this Agreement shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association.
"""
    else:  # Hindi sample
        sample_text = """
सेवा समझौता

1. दायित्व सीमा
इस समझौते के तहत कंपनी की कुल देयता पिछले 12 महीनों में ग्राहक द्वारा भुगतान की गई राशि तक सीमित होगी।

2. क्षतिपूर्ति खंड
ग्राहक सेवाओं के उपयोग से उत्पन्न किसी भी दावे, क्षति या खर्च से कंपनी को क्षतिपूर्ति, बचाव और हानि रहित रखने के लिए सहमत है।

3. स्वचालित नवीनीकरण
यह समझौता लगातार एक वर्ष की अवधि के लिए स्वचालित रूप से नवीनीकृत होगा जब तक कि ग्राहक वर्तमान अवधि के समाप्त होने से कम से कम 90 दिन पहले गैर-नवीनीकरण की लिखित सूचना प्रदान नहीं करता।

4. बौद्धिक संपदा हस्तांतरण
इस समझौते की अवधि के दौरान बनाए गए सभी कार्य उत्पाद, डिलीवरेबल्स और बौद्धिक संपदा कंपनी की विशेष संपत्ति होगी।

5. भुगतान शर्तें
सभी भुगतान गैर-वापसी योग्य हैं। ग्राहक को चालान तिथि के 15 दिनों के भीतर पूर्ण वार्षिक शुल्क का अग्रिम भुगतान करना होगा।
"""
    
    # Create a temporary "uploaded" file
    uploaded_file = io.BytesIO(sample_text.encode('utf-8'))
    uploaded_file.name = f"sample_{sample_type}.txt"
    uploaded_file.type = "text/plain"
    
    # Clear the session state
    del st.session_state['use_sample']


# Process uploaded file
if uploaded_file:
    
    # Extract text
    with st.spinner("📖 Reading contract..."):
        contract_text = extract_text(uploaded_file)
    
    if contract_text.startswith("Error"):
        st.error(contract_text)
    else:
        # Detect language
        detected_lang = detect_language(contract_text)
        lang_display = get_language_display_name(detected_lang)
        
        # Show detection result
        lang_emoji = {"en": "🇬🇧", "hi": "🇮🇳", "mixed": "🌍"}
        st.markdown(f"""
        <div class="info-banner">
            {lang_emoji.get(detected_lang, '🌐')} <strong>Language Detected:</strong> {lang_display}
        </div>
        """, unsafe_allow_html=True)
        
        # Split into clauses
        with st.spinner("✂️ Analyzing clauses..."):
            clauses = split_clauses(contract_text)
        
        if not clauses:
            st.warning("⚠️ Could not identify distinct clauses. Treating entire document as one section.")
            clauses = [contract_text]
        
        # Calculate risk score
        score_data = calculate_risk_score(clauses)
        
        # Display risk overview
        st.markdown("### 📊 Risk Assessment Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            score_color = "#4caf50" if score_data['score'] >= 70 else "#ff9800" if score_data['score'] >= 50 else "#f44336"
            st.markdown(f"""
            <div class="stat-box">
                <h1 style="color: {score_color};">{score_data['score']}</h1>
                <p>Risk Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            grade_color = "#4caf50" if score_data['grade'] in ["A+", "A"] else "#ff9800" if score_data['grade'] == "B" else "#f44336"
            st.markdown(f"""
            <div class="stat-box">
                <h1 style="color: {grade_color};">{score_data['grade']}</h1>
                <p>Grade</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-box">
                <h1>{score_data['risky_clauses']}</h1>
                <p>Risky Clauses</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-box">
                <h1 style="color: #f44336;">{score_data['high_risk_count']}</h1>
                <p>High Risk</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk breakdown
        if score_data['high_risk_count'] > 0 or score_data['medium_risk_count'] > 0:
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🔴 High Risk Items", score_data['high_risk_count'])
            with col2:
                st.metric("🟡 Medium Risk Items", score_data['medium_risk_count'])
            with col3:
                st.metric("🟢 Low Risk Items", score_data['low_risk_count'])
        
        # Overall assessment
        st.markdown("---")
        if score_data['score'] >= 80:
            st.markdown("""
            <div class="success-banner">
                ✅ <strong>Overall Assessment:</strong> This contract appears relatively safe with minimal risk factors.
            </div>
            """, unsafe_allow_html=True)
        elif score_data['score'] >= 60:
            st.markdown("""
            <div class="warning-banner">
                ⚠️ <strong>Overall Assessment:</strong> This contract has moderate risks. Review flagged clauses carefully.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-banner" style="background: #ffebee; border-left-color: #f44336;">
                🚨 <strong>Overall Assessment:</strong> This contract has significant risks. Strongly recommend legal review.
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed clause analysis
        st.markdown("---")
        st.markdown("### 🔍 Detailed Clause Analysis")
        
        # Count risky clauses
        risky_count = sum(1 for c in clauses if detect_risks(c))
        
        if risky_count == 0:
            st.success("🎉 Great news! No major risk patterns detected in this contract.")
            st.balloons()
        else:
            st.write(f"Found **{risky_count}** clauses with potential risks:")
            
            # Show risky clauses
            for i, clause in enumerate(clauses):
                risks = detect_risks(clause)
                
                if risks:
                    # Determine highest risk level
                    risk_levels = [get_risk_severity(r) for r in risks]
                    if "High" in risk_levels:
                        highest_level = "High"
                        risk_class = "high-risk"
                        risk_emoji = "🔴"
                    elif "Medium" in risk_levels:
                        highest_level = "Medium"
                        risk_class = "medium-risk"
                        risk_emoji = "🟡"
                    else:
                        highest_level = "Low"
                        risk_class = "low-risk"
                        risk_emoji = "🟢"
                    
                    # Create expandable section for each risky clause
                    with st.expander(
                        f"{risk_emoji} **Clause {i+1}**: {', '.join(risks)} ({highest_level} Risk)",
                        expanded=False
                    ):                        
                        # Show clause text
                        st.markdown("**📄 Clause Text:**")
                        clause_preview = clause[:400] + ("..." if len(clause) > 400 else "")
                        st.text_area(
                            "Clause content",
                            clause_preview,
                            height=150,
                            key=f"clause_{i}",
                            label_visibility="collapsed"
                        )
                        
                        # Show identified risks
                        st.markdown("**⚠️ Identified Risks:**")
                        for risk in risks:
                            level = get_risk_severity(risk)
                            level_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[level]
                            st.markdown(f"{level_emoji} **{risk}** - *{level} Risk*")
                        
                        st.markdown("---")
                        
                        # AI Explanation button
                        if st.button(f"🤖 Get AI Analysis", key=f"explain_{i}", use_container_width=True):
                            with st.spinner("🧠 AI is analyzing this clause..."):
                                if len(risks) > 1:
                                    explanation = explain_multiple_risks(clause, risks, output_lang)
                                else:
                                    explanation = explain_clause(clause, output_lang, risks[0])
                                
                                st.markdown("**🎓 AI Explanation:**")
                                st.markdown(explanation)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download report section
        st.markdown("---")
        st.markdown("### 📥 Export Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate text report
            report = io.StringIO()
            report.write("=" * 60 + "\n")
            report.write("CONTRACT RISK ASSESSMENT REPORT\n")
            report.write("=" * 60 + "\n\n")
            report.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"Document: {uploaded_file.name}\n")
            report.write(f"Language: {lang_display}\n")
            report.write(f"\nRISK SCORE: {score_data['score']}/100 (Grade: {score_data['grade']})\n")
            report.write(f"Total Clauses Analyzed: {score_data['total_clauses']}\n")
            report.write(f"Risky Clauses Found: {score_data['risky_clauses']}\n")
            report.write(f"  - High Risk: {score_data['high_risk_count']}\n")
            report.write(f"  - Medium Risk: {score_data['medium_risk_count']}\n")
            report.write(f"  - Low Risk: {score_data['low_risk_count']}\n")
            report.write("\n" + "=" * 60 + "\n")
            report.write("DETAILED FINDINGS\n")
            report.write("=" * 60 + "\n\n")
            
            for i, clause in enumerate(clauses):
                risks = detect_risks(clause)
                if risks:
                    report.write(f"\nCLAUSE #{i+1}\n")
                    report.write("-" * 60 + "\n")
                    report.write(f"Text: {clause[:200]}...\n\n")
                    report.write(f"Risks Identified: {', '.join(risks)}\n")
                    for risk in risks:
                        level = get_risk_severity(risk)
                        report.write(f"  - {risk}: {level} Risk\n")
                    report.write("\n")
            
            report.write("\n" + "=" * 60 + "\n")
            report.write("RECOMMENDATION\n")
            report.write("=" * 60 + "\n")
            if score_data['score'] >= 80:
                report.write("This contract appears relatively safe. Review flagged items as a precaution.\n")
            elif score_data['score'] >= 60:
                report.write("This contract has moderate risks. Carefully review all flagged clauses.\n")
            else:
                report.write("This contract has significant risks. Professional legal review is strongly recommended.\n")
            
            # Download button
            st.download_button(
                label="📄 Download Text Report",
                data=report.getvalue(),
                file_name=f"contract_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            st.info("💡 **Tip:** Share this report with your legal advisor for professional review")

else:
    # Landing state - no file uploaded
    st.markdown("""
    <div class="info-banner">
        👆 <strong>Get Started:</strong> Upload your contract document above or try a sample contract from the sidebar.
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Smart Detection
        Identifies 15+ types of risky clauses automatically using advanced pattern matching.
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 AI Explanations
        Get simple, actionable explanations powered by Claude AI for complex legal language.
        """)
    
    with col3:
        st.markdown("""
        ### 🌍 Bilingual
        Full support for English and Hindi contracts with auto-detection.
        """)
    
    st.markdown("---")
    
    # How it works
    st.markdown("### 🚀 How It Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Upload
        Upload your PDF or TXT contract document
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ Analyze
        AI scans for risky clauses and patterns
        """)
    
    with col3:
        st.markdown("""
        #### 3️⃣ Understand
        Get simple explanations of each risk
        """)
    
    with col4:
        st.markdown("""
        #### 4️⃣ Act
        Download report and take action
        """)