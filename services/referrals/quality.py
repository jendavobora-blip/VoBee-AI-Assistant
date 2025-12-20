"""
Referral quality scoring
"""

from datetime import datetime, timedelta


def calculate_quality_score(referrals: list, days_active: int = 30) -> float:
    """
    Calculate referral quality score
    
    Args:
        referrals: List of referral records
        days_active: Number of days to consider for activity
    
    Returns:
        Quality score between 0 and 1
    """
    if not referrals:
        return 0.0
    
    score = 0.0
    total_weight = 0
    
    cutoff_date = datetime.utcnow() - timedelta(days=days_active)
    
    for referral in referrals:
        created_at = referral.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        # Recent referrals score higher
        if created_at > cutoff_date:
            days_old = (datetime.utcnow() - created_at).days
            recency_weight = 1.0 - (days_old / days_active)
            score += recency_weight
            total_weight += 1
    
    if total_weight == 0:
        return 0.0
    
    return min(score / total_weight, 1.0)


def calculate_rewards(referred_count: int, quality_score: float) -> list:
    """
    Calculate rewards based on referrals
    
    Args:
        referred_count: Number of successful referrals
        quality_score: Quality score of referrals
    
    Returns:
        List of rewards
    """
    rewards = []
    
    # Basic milestones
    if referred_count >= 3:
        rewards.append({'type': 'invite_codes', 'amount': 3, 'reason': 'First 3 referrals'})
    
    if referred_count >= 10:
        rewards.append({'type': 'invite_codes', 'amount': 5, 'reason': '10 referrals milestone'})
    
    if referred_count >= 25:
        rewards.append({'type': 'premium', 'duration': '1 month', 'reason': '25 referrals milestone'})
    
    # Quality-based rewards
    if quality_score > 0.8 and referred_count >= 5:
        rewards.append({'type': 'quality_bonus', 'amount': 2, 'reason': 'High quality referrals'})
    
    return rewards
