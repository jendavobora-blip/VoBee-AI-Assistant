"""
Waitlist and Invite Service - Main Flask Application
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, timedelta
import os
import logging
import secrets
import string
import hashlib
from functools import wraps

from models import Base, WaitlistEntry, InviteCode, Referral, UserAccount, InviteBatch, QualityMetrics
from scoring import calculate_priority_score, validate_email_format, validate_email_domain, estimate_wait_time
from email_service import EmailService
from quality_gates import QualityGateMonitor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://waitlist:waitlist@postgres:5432/waitlist_db')
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Session = scoped_session(SessionLocal)

# Initialize services
email_service = EmailService()

# Admin authentication (simple token-based)
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', 'admin-secret-token-change-me')

# Rate limiting storage (simple in-memory for MVP)
rate_limit_storage = {}


def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")


def require_admin(f):
    """Decorator for admin-only endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


def check_rate_limit(ip: str, limit: int = 10, window: int = 60) -> bool:
    """
    Check rate limit for IP address
    
    Args:
        ip: IP address
        limit: Max requests per window
        window: Time window in seconds
        
    Returns:
        True if within limit, False if exceeded
    """
    now = datetime.utcnow()
    
    if ip not in rate_limit_storage:
        rate_limit_storage[ip] = []
    
    # Clean old requests outside window
    rate_limit_storage[ip] = [
        req_time for req_time in rate_limit_storage[ip]
        if (now - req_time).total_seconds() < window
    ]
    
    # Check if limit exceeded
    if len(rate_limit_storage[ip]) >= limit:
        return False
    
    # Add current request
    rate_limit_storage[ip].append(now)
    return True


def generate_invite_code() -> str:
    """Generate secure invite code in format VOBEE-{12 uppercase alphanumeric}"""
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(secrets.choice(chars) for _ in range(12))
    return f"VOBEE-{random_part}"


def sanitize_text(text: str) -> str:
    """Sanitize user input text"""
    if not text:
        return ""
    # Remove potentially dangerous characters
    text = text.strip()
    # Basic XSS prevention
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        text = text.replace(char, '')
    return text[:1000]  # Limit length


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'waitlist-service'}), 200


@app.route('/api/waitlist/join', methods=['POST'])
def join_waitlist():
    """
    Join waitlist endpoint
    
    Request body:
        - email: Email address (required)
        - use_case: Use case description (required, min 20 chars)
        - persona: User persona (required)
    """
    # Rate limiting
    ip = request.remote_addr
    if not check_rate_limit(ip):
        return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
    
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    
    # Validate required fields
    email = data.get('email', '').lower().strip()
    use_case = sanitize_text(data.get('use_case', ''))
    persona = data.get('persona', '').lower()
    
    if not email or not use_case or not persona:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate email format
    if not validate_email_format(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate use case length
    if len(use_case) < 20:
        return jsonify({'error': 'Use case must be at least 20 characters'}), 400
    
    # Validate persona
    valid_personas = ['solo_founder', 'small_team', 'agency', 'content_creator', 'other']
    if persona not in valid_personas:
        return jsonify({'error': 'Invalid persona'}), 400
    
    session = Session()
    try:
        # Check if email already exists
        existing = session.query(WaitlistEntry).filter_by(email=email).first()
        if existing:
            return jsonify({'error': 'Email already on waitlist'}), 409
        
        # Calculate priority score
        score_result = calculate_priority_score(persona, use_case, email)
        
        # Validate email domain
        if not score_result['domain_valid']:
            return jsonify({'error': 'Disposable email addresses are not allowed'}), 400
        
        # Create waitlist entry
        entry = WaitlistEntry(email=email, use_case=use_case, persona=persona)
        entry.priority_score = score_result['score']
        entry.status = 'pending'
        
        session.add(entry)
        session.commit()
        
        # Calculate position
        position = session.query(WaitlistEntry).filter(
            WaitlistEntry.priority_score > entry.priority_score
        ).count() + 1
        
        entry.position = position
        session.commit()
        
        # Get total waiting
        total_waiting = session.query(WaitlistEntry).filter_by(status='pending').count()
        
        # Estimate wait time
        estimated_wait = estimate_wait_time(position, total_waiting)
        
        # Send confirmation email
        email_service.send_waitlist_confirmation(email, position, total_waiting, estimated_wait)
        
        logger.info(f"New waitlist entry: {email} at position {position} with score {entry.priority_score}")
        
        return jsonify({
            'success': True,
            'position': position,
            'total_waiting': total_waiting,
            'estimated_wait': estimated_wait,
            'priority_score': score_result['score']
        }), 201
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error joining waitlist: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()


@app.route('/api/waitlist/stats', methods=['GET'])
@require_admin
def waitlist_stats():
    """Get waitlist statistics (admin only)"""
    session = Session()
    try:
        total = session.query(WaitlistEntry).count()
        pending = session.query(WaitlistEntry).filter_by(status='pending').count()
        invited = session.query(WaitlistEntry).filter_by(status='invited').count()
        joined = session.query(WaitlistEntry).filter_by(status='joined').count()
        
        # Stats by persona
        from sqlalchemy import func
        persona_stats = session.query(
            WaitlistEntry.persona,
            func.count(WaitlistEntry.id),
            func.avg(WaitlistEntry.priority_score)
        ).group_by(WaitlistEntry.persona).all()
        
        persona_breakdown = {
            persona: {'count': count, 'avg_score': float(avg_score or 0)}
            for persona, count, avg_score in persona_stats
        }
        
        # Average priority score
        avg_score = session.query(func.avg(WaitlistEntry.priority_score)).scalar() or 0
        
        return jsonify({
            'total': total,
            'pending': pending,
            'invited': invited,
            'joined': joined,
            'avg_priority_score': float(avg_score),
            'by_persona': persona_breakdown
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting waitlist stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()


@app.route('/api/invites/generate-batch', methods=['POST'])
@require_admin
def generate_invite_batch():
    """
    Generate batch of invite codes (admin only)
    
    Request body:
        - batch_size: Number of invites to generate (default 50)
        - created_by: Admin email
        - notes: Optional notes
    """
    data = request.json or {}
    batch_size = data.get('batch_size', 50)
    created_by = data.get('created_by', 'admin')
    notes = sanitize_text(data.get('notes', ''))
    
    session = Session()
    try:
        # Check if invites are paused
        quality_monitor = QualityGateMonitor(session)
        health = quality_monitor.get_current_health()
        
        if health['invite_pause_status']:
            return jsonify({
                'error': 'Invite generation paused due to quality gates',
                'reasons': health['pause_reasons']
            }), 423  # Locked
        
        # Get top N users from waitlist by priority score
        top_users = session.query(WaitlistEntry).filter_by(
            status='pending'
        ).order_by(
            WaitlistEntry.priority_score.desc()
        ).limit(batch_size).all()
        
        if not top_users:
            return jsonify({'error': 'No pending users in waitlist'}), 404
        
        # Generate batch ID
        batch_id = f"BATCH-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
        
        # Create batch record
        batch = InviteBatch(
            batch_id=batch_id,
            batch_size=len(top_users),
            created_by=created_by,
            notes=notes
        )
        session.add(batch)
        
        # Generate codes and send emails
        generated_codes = []
        for user in top_users:
            code = generate_invite_code()
            
            invite = InviteCode(
                code=code,
                issued_to_email=user.email,
                batch_id=batch_id
            )
            session.add(invite)
            
            # Update waitlist entry status
            user.status = 'invited'
            user.invited_at = datetime.utcnow()
            
            # Send email
            expiration_date = invite.expires_at.strftime('%Y-%m-%d %H:%M UTC')
            email_service.send_invite_ready(user.email, code, expiration_date)
            
            generated_codes.append({
                'email': user.email,
                'code': code,
                'expires_at': expiration_date
            })
            
            logger.info(f"Generated invite code {code} for {user.email}")
        
        session.commit()
        
        return jsonify({
            'success': True,
            'batch_id': batch_id,
            'generated': len(generated_codes),
            'codes': generated_codes
        }), 201
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error generating invite batch: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()


@app.route('/api/invites/validate/<code>', methods=['GET'])
def validate_invite_code(code):
    """Validate an invite code"""
    session = Session()
    try:
        invite = session.query(InviteCode).filter_by(code=code.upper()).first()
        
        if not invite:
            return jsonify({'valid': False, 'error': 'Code not found'}), 404
        
        if not invite.is_valid():
            reason = 'expired' if invite.expires_at < datetime.utcnow() else 'already used'
            return jsonify({'valid': False, 'error': f'Code is {reason}'}), 400
        
        return jsonify({
            'valid': True,
            'issued_to': invite.issued_to_email,
            'expires_at': invite.expires_at.isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error validating invite code: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()


@app.route('/api/invites/redeem', methods=['POST'])
def redeem_invite_code():
    """
    Redeem an invite code and create user account
    
    Request body:
        - code: Invite code
        - email: User email (optional, defaults to issued_to_email)
        - password: User password (min 8 chars)
    """
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    
    code = data.get('code', '').upper().strip()
    email = data.get('email', '').lower().strip()
    password = data.get('password', '')
    
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    
    if not password or len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    session = Session()
    try:
        # Find and validate invite code
        invite = session.query(InviteCode).filter_by(code=code).first()
        
        if not invite:
            return jsonify({'error': 'Invalid invite code'}), 404
        
        if not invite.is_valid():
            reason = 'expired' if invite.expires_at < datetime.utcnow() else 'already used'
            return jsonify({'error': f'Code is {reason}'}), 400
        
        # Use issued_to_email if no email provided
        if not email:
            email = invite.issued_to_email
        
        if not validate_email_format(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if user already exists
        existing_user = session.query(UserAccount).filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Account already exists'}), 409
        
        # Create user account
        user = UserAccount(
            email=email,
            tier='trial',
            referral_codes_earned=3,  # Initial 3 codes
            referral_codes_available=3
        )
        session.add(user)
        
        # Mark invite as used
        invite.used_by = email
        invite.used_at = datetime.utcnow()
        invite.status = 'used'
        
        # Update waitlist entry if exists
        waitlist_entry = session.query(WaitlistEntry).filter_by(email=invite.issued_to_email).first()
        if waitlist_entry:
            waitlist_entry.status = 'joined'
        
        session.commit()
        
        logger.info(f"Invite code {code} redeemed by {email}")
        
        return jsonify({
            'success': True,
            'email': email,
            'tier': 'trial',
            'trial_days': 14
        }), 201
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error redeeming invite code: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()


@app.route('/api/referrals/generate', methods=['POST'])
def generate_referral_code():
    """
    Generate personal referral code (authenticated users only)
    
    Request body:
        - email: User email
    """
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    
    email = data.get('email', '').lower().strip()
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    session = Session()
    try:
        # Find user
        user = session.query(UserAccount).filter_by(email=email).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check eligibility
        if not user.is_eligible_for_referrals():
            days_since_trial = (datetime.utcnow() - user.trial_started_at).days
            return jsonify({
                'error': 'Not eligible for referral codes',
                'requirements': {
                    'days_since_trial': f'{days_since_trial}/14',
                    'active_days': f'{user.active_days_count}/10',
                    'codes_available': user.referral_codes_available
                }
            }), 403
        
        # Generate referral code
        code = generate_invite_code()
        
        invite = InviteCode(
            code=code,
            issued_to_email=email,
            batch_id='REFERRAL'
        )
        session.add(invite)
        
        # Decrement available codes
        user.referral_codes_available -= 1
        
        session.commit()
        
        logger.info(f"Referral code {code} generated for {email}")
        
        return jsonify({
            'success': True,
            'code': code,
            'expires_at': invite.expires_at.isoformat(),
            'codes_remaining': user.referral_codes_available
        }), 201
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error generating referral code: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()


@app.route('/api/referrals/stats/<email>', methods=['GET'])
def referral_stats(email):
    """Get referral statistics for a user"""
    email = email.lower().strip()
    
    session = Session()
    try:
        user = session.query(UserAccount).filter_by(email=email).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Count referrals
        referral_count = session.query(Referral).filter_by(referrer_email=email).count()
        active_referrals = session.query(Referral).filter_by(
            referrer_email=email,
            status='active'
        ).count()
        
        # Calculate referral quality score (simplified)
        referral_quality = active_referrals / max(referral_count, 1)
        
        return jsonify({
            'codes_earned': user.referral_codes_earned,
            'codes_available': user.referral_codes_available,
            'referral_count': referral_count,
            'active_referrals': active_referrals,
            'referral_quality_score': round(referral_quality, 2),
            'is_eligible': user.is_eligible_for_referrals()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting referral stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()


@app.route('/api/quality/health', methods=['GET'])
@require_admin
def quality_health():
    """Get quality gate health metrics (admin only)"""
    session = Session()
    try:
        quality_monitor = QualityGateMonitor(session)
        health = quality_monitor.get_current_health()
        
        return jsonify(health), 200
        
    except Exception as e:
        logger.error(f"Error getting quality health: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()


@app.route('/api/quality/update', methods=['POST'])
@require_admin
def update_quality_metrics():
    """
    Update quality metrics (admin only)
    
    Request body:
        - dau: Daily active users
        - mau: Monthly active users
        - feature_adoption_rate: Feature adoption rate (0-1)
        - paid_conversion_rate: Paid conversion rate (0-1)
        - referral_quality_score: Referral quality score (0-1)
    """
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    
    session = Session()
    try:
        quality_monitor = QualityGateMonitor(session)
        success = quality_monitor.update_metrics(data)
        
        if success:
            health = quality_monitor.get_current_health()
            return jsonify({'success': True, 'health': health}), 200
        else:
            return jsonify({'error': 'Failed to update metrics'}), 500
            
    except Exception as e:
        logger.error(f"Error updating quality metrics: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()


# Prometheus metrics endpoint
@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus-compatible metrics endpoint"""
    session = Session()
    try:
        total_waitlist = session.query(WaitlistEntry).count()
        pending_waitlist = session.query(WaitlistEntry).filter_by(status='pending').count()
        total_invites = session.query(InviteCode).count()
        used_invites = session.query(InviteCode).filter_by(status='used').count()
        total_users = session.query(UserAccount).count()
        
        metrics_text = f"""# HELP waitlist_total Total waitlist entries
# TYPE waitlist_total gauge
waitlist_total {total_waitlist}

# HELP waitlist_pending Pending waitlist entries
# TYPE waitlist_pending gauge
waitlist_pending {pending_waitlist}

# HELP invites_total Total invite codes generated
# TYPE invites_total gauge
invites_total {total_invites}

# HELP invites_used Used invite codes
# TYPE invites_used gauge
invites_used {used_invites}

# HELP users_total Total user accounts
# TYPE users_total gauge
users_total {total_users}
"""
        return metrics_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
        logger.error(f"Error generating metrics: {str(e)}")
        return "# Error generating metrics\n", 500, {'Content-Type': 'text/plain; charset=utf-8'}
    finally:
        session.close()


if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5009))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'false').lower() == 'true')
