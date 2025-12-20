"""
Waitlist Service - Flask API for waitlist management
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor

from scoring import calculate_priority_score, estimate_wait_time
from models import WaitlistEntry

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
                CREATE TABLE IF NOT EXISTS waitlist (
                    id UUID PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    use_case TEXT NOT NULL,
                    persona VARCHAR(50) NOT NULL,
                    priority_score INTEGER DEFAULT 0,
                    position INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    invited_at TIMESTAMP
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
        'service': 'waitlist',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/waitlist/join', methods=['POST'])
def join_waitlist():
    """Join the waitlist"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['email', 'use_case', 'persona']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        email = data['email']
        use_case = data['use_case']
        persona = data['persona']
        
        # Calculate priority score
        priority_score = calculate_priority_score(email, use_case, persona)
        
        # Create waitlist entry
        entry = WaitlistEntry(
            email=email,
            use_case=use_case,
            persona=persona,
            priority_score=priority_score
        )
        
        conn = get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Check if email already exists
                cur.execute("SELECT id FROM waitlist WHERE email = %s", (email,))
                if cur.fetchone():
                    return jsonify({'error': 'Email already registered'}), 409
                
                # Insert new entry
                cur.execute("""
                    INSERT INTO waitlist (id, email, use_case, persona, priority_score, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    entry.id,
                    entry.email,
                    entry.use_case,
                    entry.persona,
                    entry.priority_score,
                    entry.created_at
                ))
                
                # Calculate position based on priority score
                cur.execute("""
                    SELECT COUNT(*) + 1 as position
                    FROM waitlist
                    WHERE priority_score > %s OR (priority_score = %s AND created_at < %s)
                """, (priority_score, priority_score, entry.created_at))
                
                position = cur.fetchone()['position']
                
                # Update position
                cur.execute("""
                    UPDATE waitlist SET position = %s WHERE id = %s
                """, (position, entry.id))
                
                # Get total waiting
                cur.execute("SELECT COUNT(*) as total FROM waitlist WHERE invited_at IS NULL")
                total_waiting = cur.fetchone()['total']
                
                conn.commit()
                
                # Estimate wait time
                estimated_wait = estimate_wait_time(position, total_waiting)
                
                return jsonify({
                    'status': 'success',
                    'position': position,
                    'total_waiting': total_waiting,
                    'estimated_wait': estimated_wait
                }), 201
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error adding to waitlist: {e}")
            return jsonify({'error': 'Failed to join waitlist'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Request processing error: {e}")
        return jsonify({'error': 'Invalid request'}), 400


@app.route('/api/waitlist/stats', methods=['GET'])
def get_stats():
    """Get waitlist statistics"""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Total waiting
                cur.execute("SELECT COUNT(*) as total FROM waitlist WHERE invited_at IS NULL")
                total = cur.fetchone()['total']
                
                # Processed today
                cur.execute("""
                    SELECT COUNT(*) as processed_today
                    FROM waitlist
                    WHERE invited_at >= CURRENT_DATE
                """)
                processed_today = cur.fetchone()['processed_today']
                
                return jsonify({
                    'total': total,
                    'processed_today': processed_today
                })
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
