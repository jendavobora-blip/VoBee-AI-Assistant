"""
Priority scoring algorithm for waitlist
"""


def calculate_priority_score(email: str, use_case: str, persona: str) -> int:
    """
    Calculate priority score for waitlist positioning
    
    Args:
        email: User's email address
        use_case: Description of intended use case
        persona: User persona type
    
    Returns:
        Priority score (higher = higher priority)
    """
    score = 0
    
    # Persona-based scoring
    persona_scores = {
        'solo_founder': 10,
        'small_team': 15,
        'agency': 20,
        'content_creator': 8,
        'other': 5
    }
    score += persona_scores.get(persona, 5)
    
    # Use case length scoring (detailed use cases get higher priority)
    if len(use_case.split()) > 20:
        score += 10
    
    # Keyword-based scoring (relevant keywords increase priority)
    keywords = ['marketing', 'content', 'automation', 'time']
    if any(word in use_case.lower() for word in keywords):
        score += 5
    
    return score


def estimate_wait_time(position: int, total_waiting: int) -> str:
    """
    Estimate wait time based on position
    
    Args:
        position: Position in waitlist
        total_waiting: Total number waiting
    
    Returns:
        Estimated wait time string
    """
    if position <= 50:
        return "1-2 days"
    elif position <= 200:
        return "1 week"
    elif position <= 500:
        return "2-3 weeks"
    elif position <= 1000:
        return "1 month"
    else:
        return "4-6 weeks"
