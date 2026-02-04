"""
Template-based risk explanations (fallback when AI is unavailable)
"""

EXPLANATIONS = {
    "Liability Cap": {
        "meaning": "The company limits how much they'll pay if something goes wrong",
        "risk": "If they cause ₹10 lakh in damages, you might only recover ₹50,000",
        "who_benefits": "The service provider/vendor",
        "action": "Negotiate for higher liability caps or remove this limitation entirely",
    },
    
    "Indemnification": {
        "meaning": "You agree to pay their legal costs if someone sues them",
        "risk": "You could pay crores in legal fees for their mistakes or actions",
        "who_benefits": "The other party (they get legal protection at your expense)",
        "action": "Request 'mutual indemnification' where both parties protect each other equally",
    },
    
    "Automatic Renewal": {
        "meaning": "Contract renews automatically unless you cancel in advance",
        "risk": "You might get locked into another year and charged automatically",
        "who_benefits": "The vendor (guaranteed recurring revenue)",
        "action": "Request advance notice (60-90 days) and opt-in renewal instead",
    },
    
    "Termination Fee": {
        "meaning": "You must pay a penalty to end the contract early",
        "risk": "Early exit could cost thousands in penalties",
        "who_benefits": "The service provider",
        "action": "Negotiate lower penalties or pro-rated refunds for unused services",
    },
    
    "IP Transfer": {
        "meaning": "All work you create or contribute becomes their property",
        "risk": "You lose ownership of your ideas, designs, or innovations",
        "who_benefits": "The company (they own everything)",
        "action": "Retain ownership or negotiate shared IP rights",
    },
    
    "Non-Compete": {
        "meaning": "You cannot work for competitors or start similar business",
        "risk": "Limits your career options and business opportunities",
        "who_benefits": "Your employer/client",
        "action": "Limit scope (geography, time, specific roles) or remove entirely",
    },
    
    "Arbitration Clause": {
        "meaning": "Disputes must go to private arbitration, not court",
        "risk": "You lose right to jury trial and public court proceedings",
        "who_benefits": "Usually the company (arbitration often favors repeat users)",
        "action": "Request mutual arbitration agreement or remove this clause",
    },
    
    "Unilateral Changes": {
        "meaning": "They can change terms anytime without your consent",
        "risk": "Prices, services, or conditions can change at their discretion",
        "who_benefits": "The service provider",
        "action": "Require written notice and right to terminate if changes are unfavorable",
    },
    
    "Limited Warranty": {
        "meaning": "Product/service sold 'as is' with no guarantees",
        "risk": "No recourse if product is defective or doesn't work",
        "who_benefits": "The seller",
        "action": "Request specific warranties or money-back guarantee",
    },
    
    "Data Rights": {
        "meaning": "Company can use your data for any purpose indefinitely",
        "risk": "Your personal or business data could be sold or misused",
        "who_benefits": "The company (monetizes your data)",
        "action": "Limit data usage to specific purposes and request deletion rights",
    },
    
    "Jurisdiction": {
        "meaning": "Legal disputes must be filed in a specific court/location",
        "risk": "You may have to travel far or hire distant lawyers",
        "who_benefits": "The party who chose the jurisdiction",
        "action": "Negotiate neutral jurisdiction or your home jurisdiction",
    },
    
    "Confidentiality Burden": {
        "meaning": "You must keep information secret forever",
        "risk": "Permanent obligation that limits your future opportunities",
        "who_benefits": "The other party",
        "action": "Set time limits (2-5 years) and define what's actually confidential",
    },
    
    "Payment Terms": {
        "meaning": "Payment is non-refundable and due upfront",
        "risk": "You lose money even if service isn't delivered",
        "who_benefits": "The vendor",
        "action": "Negotiate refund policy or milestone-based payments",
    },
    
    "Force Majeure Abuse": {
        "meaning": "Company can suspend service for broadly defined reasons",
        "risk": "Service interruptions without refunds or remedies",
        "who_benefits": "The service provider",
        "action": "Narrow the definition and ensure refunds for extended outages",
    },
    
    "Assignment Rights": {
        "meaning": "Company can transfer contract to another party without your approval",
        "risk": "You might end up dealing with unknown third party",
        "who_benefits": "The original company",
        "action": "Require your consent before contract assignment",
    },
}


def get_template_explanation(risk_type: str) -> str:
    """
    Get template-based explanation for a risk
    Used as fallback when AI is unavailable
    """
    exp = EXPLANATIONS.get(risk_type)
    
    if not exp:
        return f"""
**Meaning:** This clause contains potential risks that should be reviewed carefully.

**Risk:** Could impact your rights, obligations, or financial exposure.

**Who Benefits:** Typically favors the party that drafted the contract.

**Recommendation:** Consult with a legal professional for detailed analysis.
"""
    
    return f"""
**Meaning:** {exp['meaning']}

**Risk:** {exp['risk']}

**Who Benefits:** {exp['who_benefits']}

**Recommendation:** {exp['action']}
"""


def get_hindi_template_explanation(risk_type: str) -> str:
    """Hindi version of template explanations"""
    
    hindi_explanations = {
        "Liability Cap": {
            "meaning": "कंपनी अपनी जिम्मेदारी को सीमित करती है",
            "risk": "₹10 लाख का नुकसान होने पर भी आपको केवल ₹50,000 मिल सकते हैं",
            "who_benefits": "सेवा प्रदाता",
            "action": "उच्च सीमा के लिए बातचीत करें या इसे हटाएं",
        },
        "Indemnification": {
            "meaning": "आप उनकी कानूनी लागत चुकाने के लिए सहमत हैं",
            "risk": "उनकी गलतियों के लिए आपको करोड़ों रुपये चुकाने पड़ सकते हैं",
            "who_benefits": "दूसरी पार्टी",
            "action": "'पारस्परिक क्षतिपूर्ति' का अनुरोध करें",
        },
    }
    
    exp = hindi_explanations.get(risk_type)
    
    if not exp:
        return f"""
**अर्थ:** इस खंड में संभावित जोखिम हैं जिनकी सावधानीपूर्वक समीक्षा की जानी चाहिए।

**जोखिम:** आपके अधिकारों या वित्तीय दायित्व को प्रभावित कर सकता है।

**लाभ:** आमतौर पर अनुबंध तैयार करने वाली पार्टी को।

**सिफारिश:** विस्तृत विश्लेषण के लिए कानूनी पेशेवर से परामर्श लें।
"""
    
    return f"""
**अर्थ:** {exp['meaning']}

**जोखिम:** {exp['risk']}

**लाभ:** {exp['who_benefits']}

**सिफारिश:** {exp['action']}
"""