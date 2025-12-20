"""
Secure invite code generation
"""

import secrets
import hashlib


def generate_invite_code() -> str:
    """
    Generate a secure invite code
    
    Returns:
        Invite code in format VOBEE-XXXXXXXXXXXX
    """
    random_bytes = secrets.token_bytes(16)
    hash_digest = hashlib.sha256(random_bytes).hexdigest()
    return f"VOBEE-{hash_digest[:12].upper()}"


def generate_batch(batch_size: int) -> list:
    """
    Generate a batch of invite codes
    
    Args:
        batch_size: Number of codes to generate
    
    Returns:
        List of invite codes
    """
    return [generate_invite_code() for _ in range(batch_size)]
