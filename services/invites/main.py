"""
Invite Code Service - Flask API for invite code management
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime, timedelta
import os
import psycopg2
from psycopg2.extras import RealDictCursor

from generator import generate_batch
from models import InviteCode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://orchestrator:postgres@postgres:5432/orchestrator_db')


def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS invite_codes (
                    code VARCHAR(20) PRIMARY KEY,
                    issued_to VARCHAR(255),
                    batch_id VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    used_by VARCHAR(255),
                    used_at TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'active'
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
        'service': 'invites',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/invites/generate', methods=['POST'])
def generate_codes():
    """Generate a batch of invite codes"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'batch_size' not in data:
            return jsonify({'error': 'Missing batch_size'}), 400
        
        batch_size = data['batch_size']
        batch_id = data.get('batch_id', f"BATCH-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
        
        if batch_size <= 0 or batch_size > 1000:
            return jsonify({'error': 'Invalid batch_size (must be 1-1000)'}), 400
        
        # Generate codes
        codes = generate_batch(batch_size)
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # Insert codes
                for code in codes:
                    invite = InviteCode(code=code, batch_id=batch_id)
                    cur.execute("""
                        INSERT INTO invite_codes (code, batch_id, created_at, expires_at, status)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        invite.code,
                        invite.batch_id,
                        invite.created_at,
                        invite.expires_at,
                        invite.status
                    ))
                
                conn.commit()
                
                return jsonify({
                    'status': 'success',
                    'batch_id': batch_id,
                    'generated': batch_size,
                    'codes': codes
                }), 201
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error generating codes: {e}")
            return jsonify({'error': 'Failed to generate codes'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Request processing error: {e}")
        return jsonify({'error': 'Invalid request'}), 400


@app.route('/api/invites/redeem', methods=['POST'])
def redeem_code():
    """Redeem an invite code"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['code', 'email']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        code = data['code']
        email = data['email']
        
        conn = get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Get code
                cur.execute("SELECT * FROM invite_codes WHERE code = %s", (code,))
                result = cur.fetchone()
                
                if not result:
                    return jsonify({'error': 'Invalid code'}), 404
                
                invite = InviteCode.from_dict(dict(result))
                
                # Validate code
                if not invite.is_valid():
                    if invite.used_at:
                        return jsonify({'error': 'Code already used'}), 400
                    elif datetime.utcnow() > invite.expires_at:
                        return jsonify({'error': 'Code expired'}), 400
                    else:
                        return jsonify({'error': 'Code not valid'}), 400
                
                # Redeem code
                cur.execute("""
                    UPDATE invite_codes
                    SET used_by = %s, used_at = %s, status = 'used'
                    WHERE code = %s
                """, (email, datetime.utcnow(), code))
                
                conn.commit()
                
                return jsonify({
                    'status': 'success',
                    'message': 'Invite code redeemed successfully',
                    'email': email
                }), 200
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error redeeming code: {e}")
            return jsonify({'error': 'Failed to redeem code'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Request processing error: {e}")
        return jsonify({'error': 'Invalid request'}), 400


@app.route('/api/invites/<code>/status', methods=['GET'])
def get_code_status(code):
    """Get invite code status"""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM invite_codes WHERE code = %s", (code,))
                result = cur.fetchone()
                
                if not result:
                    return jsonify({'error': 'Code not found'}), 404
                
                invite = InviteCode.from_dict(dict(result))
                
                return jsonify({
                    'valid': invite.is_valid(),
                    'expires_at': invite.expires_at.isoformat(),
                    'used': invite.used_at is not None,
                    'status': invite.status
                })
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error getting code status: {e}")
        return jsonify({'error': 'Failed to get status'}), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
