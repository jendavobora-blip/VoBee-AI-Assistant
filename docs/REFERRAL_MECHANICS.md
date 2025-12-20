# Referral Mechanics Guide

## Overview

The VoBee referral system rewards users for bringing quality users to the platform. It tracks referral chains, calculates quality scores, and distributes rewards based on engagement and value.

## How It Works

### 1. User Journey

```
New User → Joins Waitlist → Receives Invite → Uses Platform (14 days) → Earns Codes → Refers Others
```

### 2. Earning Invite Codes

Users earn invite codes through:

- **Time-based**: After 14 days of active platform usage
- **Referral-based**: Making successful referrals
- **Quality-based**: Maintaining high referral quality scores

### 3. Referral Quality Scoring

Quality scores (0.0 to 1.0) are calculated based on:

```python
def calculate_quality_score(referrals, days_active=30):
    score = 0.0
    total_weight = 0
    cutoff_date = datetime.utcnow() - timedelta(days=days_active)
    
    for referral in referrals:
        created_at = referral['created_at']
        
        # Recent referrals score higher
        if created_at > cutoff_date:
            days_old = (datetime.utcnow() - created_at).days
            recency_weight = 1.0 - (days_old / days_active)
            score += recency_weight
            total_weight += 1
    
    return min(score / total_weight, 1.0) if total_weight > 0 else 0.0
```

### Factors Affecting Quality:

1. **Recency**: Recent referrals score higher
2. **Activity**: How engaged referred users are
3. **Retention**: Whether referred users stay active
4. **Conversion**: Whether referred users complete onboarding

## Reward Tiers

### Basic Milestones

| Referrals | Reward | Type |
|-----------|--------|------|
| 3 | 3 invite codes | Codes |
| 10 | 5 invite codes | Codes |
| 25 | 1 month premium | Premium Access |
| 50 | 10 invite codes + 3 months premium | Combo |
| 100 | Lifetime premium | Premium Access |

### Quality Bonuses

High-quality referrers (quality_score > 0.8) with 5+ referrals earn:
- 2 bonus invite codes
- Priority support access
- Feature preview access

## API Usage

### Check Earned Codes

```bash
curl -X POST http://localhost:8000/api/referrals/earn \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "user@example.com"
  }'
```

Response:
```json
{
  "earned": true,
  "codes_available": 3,
  "message": "You earned 3 invite codes after 14 days of usage"
}
```

### Track Referral

```bash
curl -X POST http://localhost:8000/api/referrals/share \
  -H "Content-Type: application/json" \
  -d '{
    "inviter_email": "user@example.com",
    "recipient_email": "friend@example.com",
    "invite_code": "VOBEE-A7F3E9D2B1C4"
  }'
```

Response:
```json
{
  "status": "success",
  "referral_id": "uuid",
  "message": "Referral tracked successfully"
}
```

### Get Quality Metrics

```bash
curl http://localhost:8000/api/referrals/user@example.com/quality
```

Response:
```json
{
  "referred_count": 5,
  "quality_score": 0.82,
  "rewards": [
    {
      "type": "invite_codes",
      "amount": 3,
      "reason": "First 3 referrals"
    },
    {
      "type": "quality_bonus",
      "amount": 2,
      "reason": "High quality referrals"
    }
  ]
}
```

## Referral Chain Tracking

The system tracks complete referral chains to understand network effects:

```
User A → User B → User C → User D
```

This enables:
- Network growth analysis
- Influencer identification
- Viral coefficient calculation
- Multi-level rewards (future feature)

### Database Structure

```sql
CREATE TABLE referrals (
    id UUID PRIMARY KEY,
    inviter_email VARCHAR(255) NOT NULL,
    invited_email VARCHAR(255) NOT NULL,
    invite_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient queries
CREATE INDEX idx_referrals_inviter ON referrals(inviter_email);
CREATE INDEX idx_referrals_invited ON referrals(invited_email);
```

## Best Practices for Referrers

### 1. Target the Right Audience

Refer people who will:
- Actively use the platform
- Benefit from the features
- Stay engaged long-term

### 2. Provide Context

When sharing invite codes:
- Explain what VoBee does
- Share your own experience
- Highlight specific benefits

### 3. Follow Up

After referrals join:
- Check if they need help
- Share tips and best practices
- Keep them engaged

### 4. Quality Over Quantity

Focus on quality referrals rather than mass invites:
- Better quality score
- More rewards
- Sustainable growth

## Anti-Abuse Measures

### Detection

The system monitors for:
- Fake email addresses
- Inactive accounts
- Pattern matching (e.g., user+1@domain.com)
- Rapid bulk referrals
- Low engagement rates

### Consequences

Abuse results in:
1. Warning on first offense
2. Temporary suspension of referral privileges
3. Permanent ban for severe violations
4. Revocation of earned rewards

### Quality Thresholds

Minimum quality score requirements:
- < 0.3: Warning issued
- < 0.2: Referral rewards paused
- < 0.1: Account review triggered

## Analytics & Reporting

### Key Metrics

Track your referral performance:

1. **Conversion Rate**: % of invites that sign up
2. **Activation Rate**: % of signups that become active
3. **Retention Rate**: % of referrals still active after 30 days
4. **Quality Score**: Overall referral quality
5. **Total Value**: Combined lifetime value of referrals

### Dashboard Access

```
GET /api/referrals/{email}/analytics
```

Returns:
- Historical referral data
- Quality score trends
- Reward history
- Projected future rewards

## Email Notifications

Users receive emails for:

### Earned Rewards
- Notification when codes are earned
- Current reward balance
- Next milestone progress

### Referral Activity
- When someone uses your code
- When a referral becomes active
- Milestone achievements

### Quality Updates
- Monthly quality score report
- Suggestions for improvement
- Bonus opportunities

## Integration with Other Services

### With Invite Code Service
- Generates codes for earned rewards
- Validates codes during redemption
- Tracks code usage per referrer

### With Quality Gates
- Quality scores feed into trust calculations
- High-quality referrers can unlock system features
- Poor quality triggers investigations

### With Waitlist
- Priority boost for referred users
- Automatic approval for high-quality referrers
- Fast-track processing

## Future Enhancements

1. **Multi-level Rewards**: Earn from referrals of referrals
2. **Leaderboards**: Compete with other referrers
3. **Custom Codes**: Personalized invite codes
4. **Analytics Dashboard**: Detailed performance metrics
5. **Automated Optimization**: ML-powered referral suggestions
6. **Social Sharing**: One-click social media integration
7. **Team Referrals**: Coordinated referral campaigns

## Support

For referral-related questions:
- Email: referrals@vobee.ai
- Documentation: /docs/referrals
- API Reference: /api/docs#referrals

## Terms & Conditions

1. Rewards are subject to quality verification
2. Abuse results in reward forfeiture
3. VoBee reserves the right to modify rewards
4. Referral codes are non-transferable
5. Quality scores are calculated automatically
6. Appeals can be submitted for review
