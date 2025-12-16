"""
Confirmation Handler - Simplified yes/no confirmation module
"""

from typing import Dict, Any, Optional, Callable
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ConfirmationHandler:
    """
    Simplified confirmation handler for yes/no decisions
    Implements non-merge prohibited interaction layer
    """
    
    def __init__(self):
        self.pending_confirmations: Dict[str, Dict[str, Any]] = {}
        self.confirmation_history: list = []
        logger.info("ConfirmationHandler initialized")
    
    def request_confirmation(
        self,
        confirmation_id: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        timeout_seconds: Optional[int] = None,
        on_confirm: Optional[Callable] = None,
        on_reject: Optional[Callable] = None
    ) -> str:
        """
        Request a yes/no confirmation
        
        Args:
            confirmation_id: Unique confirmation identifier
            message: Confirmation message/question
            context: Additional context data
            timeout_seconds: Auto-timeout in seconds
            on_confirm: Callback function for confirmation
            on_reject: Callback function for rejection
            
        Returns:
            Confirmation ID
        """
        from datetime import timedelta
        
        confirmation = {
            'confirmation_id': confirmation_id,
            'message': message,
            'context': context or {},
            'status': 'pending',
            'requested_at': datetime.utcnow().isoformat(),
            'resolved_at': None,
            'response': None,
            'on_confirm': on_confirm,
            'on_reject': on_reject
        }
        
        if timeout_seconds:
            timeout_time = datetime.utcnow() + timedelta(seconds=timeout_seconds)
            confirmation['timeout_at'] = timeout_time.isoformat()
        else:
            confirmation['timeout_at'] = None
        
        self.pending_confirmations[confirmation_id] = confirmation
        
        logger.info(
            f"Requested confirmation {confirmation_id}: {message}"
        )
        
        return confirmation_id
    
    def confirm(self, confirmation_id: str, note: Optional[str] = None) -> bool:
        """
        Confirm with YES
        
        Args:
            confirmation_id: Confirmation identifier
            note: Optional note
            
        Returns:
            True if confirmation successful
        """
        if confirmation_id not in self.pending_confirmations:
            logger.error(f"Confirmation {confirmation_id} not found")
            return False
        
        confirmation = self.pending_confirmations[confirmation_id]
        
        if confirmation['status'] != 'pending':
            logger.warning(
                f"Confirmation {confirmation_id} already resolved: "
                f"{confirmation['status']}"
            )
            return False
        
        # Check timeout
        if self._check_timeout(confirmation):
            return False
        
        # Update confirmation
        confirmation['status'] = 'confirmed'
        confirmation['response'] = 'yes'
        confirmation['resolved_at'] = datetime.utcnow().isoformat()
        confirmation['note'] = note
        
        # Execute callback if provided
        if confirmation['on_confirm']:
            try:
                confirmation['on_confirm']()
            except Exception as e:
                logger.error(f"Error in on_confirm callback: {e}")
        
        # Move to history
        self._archive_confirmation(confirmation_id)
        
        logger.info(f"Confirmation {confirmation_id} confirmed (YES)")
        return True
    
    def reject(self, confirmation_id: str, reason: Optional[str] = None) -> bool:
        """
        Reject with NO
        
        Args:
            confirmation_id: Confirmation identifier
            reason: Optional rejection reason
            
        Returns:
            True if rejection successful
        """
        if confirmation_id not in self.pending_confirmations:
            logger.error(f"Confirmation {confirmation_id} not found")
            return False
        
        confirmation = self.pending_confirmations[confirmation_id]
        
        if confirmation['status'] != 'pending':
            logger.warning(
                f"Confirmation {confirmation_id} already resolved: "
                f"{confirmation['status']}"
            )
            return False
        
        # Update confirmation
        confirmation['status'] = 'rejected'
        confirmation['response'] = 'no'
        confirmation['resolved_at'] = datetime.utcnow().isoformat()
        confirmation['reason'] = reason
        
        # Execute callback if provided
        if confirmation['on_reject']:
            try:
                confirmation['on_reject']()
            except Exception as e:
                logger.error(f"Error in on_reject callback: {e}")
        
        # Move to history
        self._archive_confirmation(confirmation_id)
        
        logger.info(f"Confirmation {confirmation_id} rejected (NO)")
        return True
    
    def cancel(self, confirmation_id: str) -> bool:
        """Cancel a pending confirmation"""
        if confirmation_id not in self.pending_confirmations:
            return False
        
        confirmation = self.pending_confirmations[confirmation_id]
        confirmation['status'] = 'cancelled'
        confirmation['resolved_at'] = datetime.utcnow().isoformat()
        
        self._archive_confirmation(confirmation_id)
        
        logger.info(f"Confirmation {confirmation_id} cancelled")
        return True
    
    def get_confirmation(self, confirmation_id: str) -> Optional[Dict[str, Any]]:
        """Get confirmation details"""
        # Check pending first
        if confirmation_id in self.pending_confirmations:
            return self.pending_confirmations[confirmation_id].copy()
        
        # Check history
        for conf in self.confirmation_history:
            if conf['confirmation_id'] == confirmation_id:
                return conf.copy()
        
        return None
    
    def get_pending_confirmations(self) -> list:
        """Get all pending confirmations"""
        self._cleanup_timeouts()  # Clean up expired first
        return list(self.pending_confirmations.values())
    
    def _check_timeout(self, confirmation: Dict[str, Any]) -> bool:
        """Check if confirmation has timed out"""
        if not confirmation.get('timeout_at'):
            return False
        
        timeout = datetime.fromisoformat(confirmation['timeout_at'])
        if datetime.utcnow() > timeout:
            confirmation['status'] = 'timeout'
            confirmation['resolved_at'] = datetime.utcnow().isoformat()
            logger.info(
                f"Confirmation {confirmation['confirmation_id']} timed out"
            )
            return True
        
        return False
    
    def _cleanup_timeouts(self):
        """Clean up timed out confirmations"""
        to_archive = []
        
        for conf_id, confirmation in self.pending_confirmations.items():
            if self._check_timeout(confirmation):
                to_archive.append(conf_id)
        
        for conf_id in to_archive:
            self._archive_confirmation(conf_id)
    
    def _archive_confirmation(self, confirmation_id: str):
        """Move confirmation to history"""
        if confirmation_id in self.pending_confirmations:
            confirmation = self.pending_confirmations.pop(confirmation_id)
            # Remove callbacks before archiving (not serializable)
            confirmation.pop('on_confirm', None)
            confirmation.pop('on_reject', None)
            self.confirmation_history.append(confirmation)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get confirmation statistics"""
        self._cleanup_timeouts()
        
        total = len(self.pending_confirmations) + len(self.confirmation_history)
        pending = len(self.pending_confirmations)
        
        # Count statuses in history
        status_counts = {
            'confirmed': 0,
            'rejected': 0,
            'timeout': 0,
            'cancelled': 0
        }
        
        for conf in self.confirmation_history:
            status = conf['status']
            if status in status_counts:
                status_counts[status] += 1
        
        return {
            'total_confirmations': total,
            'pending': pending,
            'confirmed': status_counts['confirmed'],
            'rejected': status_counts['rejected'],
            'timeout': status_counts['timeout'],
            'cancelled': status_counts['cancelled'],
            'timestamp': datetime.utcnow().isoformat()
        }
