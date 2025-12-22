"""
Passkey Identity Management
Provides WebAuthn-based authentication without passwords
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import secrets
from jose import jwt

logger = logging.getLogger(__name__)

# Mock mode configuration
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
JWT_SECRET = os.getenv("JWT_SECRET", "vobio-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"


class IdentityManager:
    """Manages user identity and authentication"""
    
    def __init__(self):
        self.users_db = {}  # In-memory user store for mock mode
        self.sessions = {}  # Active sessions
        
    def create_mock_user(self, user_id: str, username: str) -> Dict[str, Any]:
        """Create a mock user for testing"""
        user = {
            "user_id": user_id,
            "username": username,
            "created_at": datetime.utcnow().isoformat(),
            "passkey_credential_id": f"mock-cred-{secrets.token_urlsafe(16)}",
            "public_key": "mock-public-key",
        }
        self.users_db[user_id] = user
        logger.info(f"Mock user created: {user_id}")
        return user
    
    def authenticate_passkey(self, credential_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Authenticate using passkey (mock implementation)"""
        
        if MOCK_MODE:
            # In mock mode, accept any credential and create user
            user_id = credential_data.get("user_id", f"user-{secrets.token_urlsafe(8)}")
            username = credential_data.get("username", "Mock User")
            
            if user_id not in self.users_db:
                user = self.create_mock_user(user_id, username)
            else:
                user = self.users_db[user_id]
            
            # Create session token
            token = self.create_session_token(user_id)
            
            return {
                "user": user,
                "token": token,
                "expires_in": 86400  # 24 hours
            }
        
        # Real passkey authentication would go here
        raise NotImplementedError("Real passkey authentication not implemented")
    
    def create_session_token(self, user_id: str) -> str:
        """Create a JWT session token"""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        self.sessions[token] = user_id
        return token
    
    def verify_session(self, token: str) -> Optional[str]:
        """Verify session token and return user_id"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("user_id")
            
            # Check if session exists
            if token in self.sessions:
                return user_id
            
            return None
        except Exception as e:
            logger.warning(f"Token verification failed: {e}")
            return None
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return self.users_db.get(user_id)
    
    def logout(self, token: str):
        """Invalidate session"""
        if token in self.sessions:
            del self.sessions[token]
            logger.info("Session invalidated")


# Global instance
_identity_manager = None


def get_identity_manager() -> IdentityManager:
    """Get or create the global IdentityManager instance"""
    global _identity_manager
    if _identity_manager is None:
        _identity_manager = IdentityManager()
    return _identity_manager
