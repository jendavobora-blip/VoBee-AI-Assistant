"""
Priority scoring algorithm for waitlist entries
"""

import re
from typing import Dict

# Persona weights
PERSONA_WEIGHTS = {
    'agency': 20,
    'small_team': 15,
    'solo_founder': 10,
    'content_creator': 8,
    'other': 5
}

# High-intent keywords that indicate serious usage
HIGH_INTENT_KEYWORDS = [
    'business', 'client', 'customer', 'production', 'team', 'workflow',
    'automate', 'scale', 'revenue', 'productivity', 'professional',
    'enterprise', 'agency', 'company', 'startup', 'project', 'management',
    'klient', 'zákazník', 'tým', 'produkce', 'automatizace', 'firma',
    'podnikání', 'projekt', 'profesionální'  # Czech keywords
]

# Disposable email domains to reject
DISPOSABLE_DOMAINS = [
    'tempmail.com', 'throwaway.email', '10minutemail.com', 'guerrillamail.com',
    'mailinator.com', 'maildrop.cc', 'temp-mail.org', 'yopmail.com',
    'fakeinbox.com', 'trashmail.com', 'mailnesia.com', 'mintemail.com',
    'sharklasers.com', 'guerrillamail.info', 'spam4.me'
]


def calculate_priority_score(persona: str, use_case: str, email: str) -> Dict:
    """
    Calculate priority score for a waitlist entry
    
    Args:
        persona: User persona type
        use_case: User's use case description
        email: User's email address
        
    Returns:
        Dictionary with score and breakdown
    """
    score = 0.0
    breakdown = {}
    
    # Base score from persona
    persona_score = PERSONA_WEIGHTS.get(persona, 5)
    score += persona_score
    breakdown['persona'] = persona_score
    
    # Use case quality scoring
    use_case_lower = use_case.lower()
    use_case_score = 0
    
    # Check length (detailed use cases)
    word_count = len(use_case.split())
    if word_count >= 30:
        use_case_score += 10
        breakdown['detailed_use_case'] = 10
    elif word_count >= 15:
        use_case_score += 5
        breakdown['detailed_use_case'] = 5
    
    # Check for high-intent keywords
    keyword_matches = sum(1 for keyword in HIGH_INTENT_KEYWORDS if keyword in use_case_lower)
    if keyword_matches >= 3:
        use_case_score += 5
        breakdown['high_intent_keywords'] = 5
    elif keyword_matches >= 1:
        use_case_score += 3
        breakdown['high_intent_keywords'] = 3
    
    score += use_case_score
    
    # Email domain validation
    domain_valid = validate_email_domain(email)
    breakdown['domain_valid'] = domain_valid
    
    breakdown['total'] = score
    
    return {
        'score': score,
        'breakdown': breakdown,
        'domain_valid': domain_valid
    }


def validate_email_domain(email: str) -> bool:
    """
    Validate email domain is not disposable
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False if disposable
    """
    if not email or '@' not in email:
        return False
    
    domain = email.split('@')[1].lower()
    
    # Check against disposable domains list
    if domain in DISPOSABLE_DOMAINS:
        return False
    
    # Additional checks for common disposable patterns
    disposable_patterns = [
        r'temp.*mail',
        r'fake.*mail',
        r'trash.*mail',
        r'.*\.tk$',  # Free TLDs often used for disposable
    ]
    
    for pattern in disposable_patterns:
        if re.search(pattern, domain):
            return False
    
    return True


def validate_email_format(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def estimate_wait_time(position: int, total_waiting: int) -> str:
    """
    Estimate wait time based on position and total waiting
    
    Args:
        position: User's position in queue
        total_waiting: Total number of people waiting
        
    Returns:
        Human-readable wait time estimate
    """
    # Assume we invite ~50 people per week
    weekly_invites = 50
    weeks = position / weekly_invites
    
    if weeks < 1:
        return "méně než týden / less than a week"
    elif weeks < 2:
        return "1-2 týdny / 1-2 weeks"
    elif weeks < 4:
        return "2-4 týdny / 2-4 weeks"
    elif weeks < 8:
        return "1-2 měsíce / 1-2 months"
    else:
        return "2+ měsíce / 2+ months"
