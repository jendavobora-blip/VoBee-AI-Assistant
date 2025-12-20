"""
Referral Service - Flask API for referral tracking
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime, timedelta
import os
import psycopg2
from psycopg2.extras import RealDictCursor

from quality import calculate_quality_score, calculate_rewards
from models import Referral

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable must be set")


def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS referrals (
                    id UUID PRIMARY KEY,
                    inviter_email VARCHAR(255) NOT NULL,
                    invited_email VARCHAR(255) NOT NULL,
                    invite_code VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            logger.info("Database tables initialized")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        conn.rollback()
    finally:
        conn.close()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'referrals',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/referrals/earn', methods=['POST'])
def earn_codes():
    """Check if user has earned invite codes"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'user_email' not in data:
            return jsonify({'error': 'Missing user_email'}), 400
        
        user_email = data['user_email']
        
        conn = get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Get user's referral count
                cur.execute("""
                    SELECT COUNT(*) as count
                    FROM referrals
                    WHERE inviter_email = %s
                """, (user_email,))
                
                result = cur.fetchone()
                referred_count = result['count']
                
                # Simple rule: earn 3 codes after 14 days of usage
                # For this implementation, we'll base it on referral count
                codes_earned = 0
                if referred_count >= 3:
                    codes_earned = 3
                elif referred_count >= 1:
                    codes_earned = 1
                
                return jsonify({
                    'earned': codes_earned > 0,
                    'codes_available': codes_earned,
                    'message': f'You earned {codes_earned} invite codes' if codes_earned > 0 else 'Keep referring to earn codes'
                })
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error checking earned codes: {e}")
        return jsonify({'error': 'Failed to check earned codes'}), 500


@app.route('/api/referrals/share', methods=['POST'])
def share_referral():
    """Track a referral share"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['inviter_email', 'recipient_email']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        inviter_email = data['inviter_email']
        recipient_email = data['recipient_email']
        invite_code = data.get('invite_code')
        
        # Create referral
        referral = Referral(
            inviter_email=inviter_email,
            invited_email=recipient_email,
            invite_code=invite_code
        )
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # Insert referral
                cur.execute("""
                    INSERT INTO referrals (id, inviter_email, invited_email, invite_code, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    referral.id,
                    referral.inviter_email,
                    referral.invited_email,
                    referral.invite_code,
                    referral.created_at
                ))
                
                conn.commit()
                
                return jsonify({
                    'status': 'success',
                    'referral_id': referral.id,
                    'message': 'Referral tracked successfully'
                }), 201
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error tracking referral: {e}")
            return jsonify({'error': 'Failed to track referral'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Request processing error: {e}")
        return jsonify({'error': 'Invalid request'}), 400


@app.route('/api/referrals/<email>/quality', methods=['GET'])
def get_quality(email):
    """Get referral quality metrics for a user"""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Get all referrals for user
                cur.execute("""
                    SELECT *
                    FROM referrals
                    WHERE inviter_email = %s
                    ORDER BY created_at DESC
                """, (email,))
                
                referrals = [dict(row) for row in cur.fetchall()]
                referred_count = len(referrals)
                
                # Calculate quality score
                quality_score = calculate_quality_score(referrals)
                
                # Calculate rewards
                rewards = calculate_rewards(referred_count, quality_score)
                
                return jsonify({
                    'referred_count': referred_count,
                    'quality_score': quality_score,
                    'rewards': rewards
                })
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error getting quality metrics: {e}")
        return jsonify({'error': 'Failed to get quality metrics'}), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
