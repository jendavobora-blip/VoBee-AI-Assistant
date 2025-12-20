"""
Quality gate monitoring and health metrics calculation
"""

from datetime import datetime, timedelta
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class QualityGateMonitor:
    """Monitor system health and quality metrics"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.trust_score_threshold = 0.75
        self.churn_threshold = 0.20  # 20%
        self.resume_trust_threshold = 0.80
        self.resume_churn_threshold = 0.15  # 15%
    
    def calculate_trust_score(self, metrics: Dict) -> float:
        """
        Calculate trust score based on weighted metrics
        
        Formula: DAU/MAU (0.3) + feature_adoption (0.2) + paid_conversion (0.3) + referral_quality (0.2)
        
        Args:
            metrics: Dictionary with dau, mau, feature_adoption, paid_conversion, referral_quality
            
        Returns:
            Trust score (0-1)
        """
        dau = metrics.get('dau', 0)
        mau = metrics.get('mau', 1)  # Avoid division by zero
        feature_adoption = metrics.get('feature_adoption_rate', 0)
        paid_conversion = metrics.get('paid_conversion_rate', 0)
        referral_quality = metrics.get('referral_quality_score', 0)
        
        # Calculate DAU/MAU ratio
        dau_mau_ratio = dau / mau if mau > 0 else 0
        
        # Weighted trust score
        trust_score = (
            dau_mau_ratio * 0.3 +
            feature_adoption * 0.2 +
            paid_conversion * 0.3 +
            referral_quality * 0.2
        )
        
        return min(trust_score, 1.0)
    
    def calculate_churn_rate_30d(self) -> float:
        """
        Calculate 30-day churn rate
        
        Returns:
            Churn rate (0-1)
        """
        from models import UserAccount
        
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        sixty_days_ago = datetime.utcnow() - timedelta(days=60)
        
        # Users who were active 30-60 days ago
        active_30_60_days = self.db.query(UserAccount).filter(
            UserAccount.last_active_at >= sixty_days_ago,
            UserAccount.last_active_at < thirty_days_ago
        ).count()
        
        if active_30_60_days == 0:
            return 0.0
        
        # Users from that cohort who are still active in last 30 days
        still_active = self.db.query(UserAccount).filter(
            UserAccount.created_at < thirty_days_ago,
            UserAccount.last_active_at >= thirty_days_ago
        ).count()
        
        churned = active_30_60_days - still_active
        churn_rate = churned / active_30_60_days if active_30_60_days > 0 else 0
        
        return max(0, min(churn_rate, 1.0))
    
    def check_quality_gates(self, trust_score: float, churn_rate: float) -> Dict:
        """
        Check if quality gates should pause invites
        
        Args:
            trust_score: Current trust score (0-1)
            churn_rate: Current 30-day churn rate (0-1)
            
        Returns:
            Dictionary with pause status and reasons
        """
        should_pause = False
        reasons = []
        
        if trust_score < self.trust_score_threshold:
            should_pause = True
            reasons.append(f"Trust score below threshold ({trust_score:.2f} < {self.trust_score_threshold})")
            logger.warning(f"Quality gate triggered: Low trust score {trust_score:.2f}")
        
        if churn_rate > self.churn_threshold:
            should_pause = True
            reasons.append(f"Churn rate above threshold ({churn_rate:.2%} > {self.churn_threshold:.0%})")
            logger.warning(f"Quality gate triggered: High churn rate {churn_rate:.2%}")
        
        return {
            'should_pause': should_pause,
            'reasons': reasons,
            'trust_score': trust_score,
            'churn_rate': churn_rate
        }
    
    def check_resume_conditions(self, trust_score: float, churn_rate: float) -> bool:
        """
        Check if conditions are met to resume invites
        
        Args:
            trust_score: Current trust score (0-1)
            churn_rate: Current 30-day churn rate (0-1)
            
        Returns:
            True if can resume, False otherwise
        """
        can_resume = (
            trust_score > self.resume_trust_threshold and
            churn_rate < self.resume_churn_threshold
        )
        
        if can_resume:
            logger.info(f"Quality gates recovered: trust={trust_score:.2f}, churn={churn_rate:.2%}")
        
        return can_resume
    
    def get_current_health(self) -> Dict:
        """
        Get current system health metrics
        
        Returns:
            Dictionary with all health metrics
        """
        from models import QualityMetrics, UserAccount
        
        # Get latest metrics or create default
        latest_metrics = self.db.query(QualityMetrics).order_by(
            QualityMetrics.recorded_at.desc()
        ).first()
        
        if not latest_metrics:
            # Calculate initial metrics
            total_users = self.db.query(UserAccount).count()
            dau = self.db.query(UserAccount).filter(
                UserAccount.last_active_at >= datetime.utcnow() - timedelta(days=1)
            ).count()
            mau = self.db.query(UserAccount).filter(
                UserAccount.last_active_at >= datetime.utcnow() - timedelta(days=30)
            ).count()
            
            metrics_dict = {
                'dau': dau,
                'mau': max(mau, 1),
                'feature_adoption_rate': 0.5,  # Default
                'paid_conversion_rate': 0.0,
                'referral_quality_score': 0.5
            }
        else:
            metrics_dict = {
                'dau': latest_metrics.dau,
                'mau': max(latest_metrics.mau, 1),
                'feature_adoption_rate': latest_metrics.feature_adoption_rate,
                'paid_conversion_rate': latest_metrics.paid_conversion_rate,
                'referral_quality_score': latest_metrics.referral_quality_score
            }
        
        trust_score = self.calculate_trust_score(metrics_dict)
        churn_rate = self.calculate_churn_rate_30d()
        quality_check = self.check_quality_gates(trust_score, churn_rate)
        
        return {
            'trust_score': trust_score,
            'churn_rate': churn_rate,
            'dau': metrics_dict['dau'],
            'mau': metrics_dict['mau'],
            'feature_adoption_rate': metrics_dict['feature_adoption_rate'],
            'paid_conversion_rate': metrics_dict['paid_conversion_rate'],
            'referral_quality_score': metrics_dict['referral_quality_score'],
            'invite_pause_status': quality_check['should_pause'],
            'pause_reasons': quality_check['reasons']
        }
    
    def update_metrics(self, metrics: Dict) -> bool:
        """
        Update quality metrics in database
        
        Args:
            metrics: Dictionary with metric values
            
        Returns:
            True if successful
        """
        from models import QualityMetrics
        
        try:
            trust_score = self.calculate_trust_score(metrics)
            churn_rate = self.calculate_churn_rate_30d()
            quality_check = self.check_quality_gates(trust_score, churn_rate)
            
            new_metrics = QualityMetrics(
                dau=metrics.get('dau', 0),
                mau=metrics.get('mau', 0),
                feature_adoption_rate=metrics.get('feature_adoption_rate', 0),
                paid_conversion_rate=metrics.get('paid_conversion_rate', 0),
                referral_quality_score=metrics.get('referral_quality_score', 0),
                trust_score=trust_score,
                churn_rate_30d=churn_rate,
                invite_pause_status=quality_check['should_pause']
            )
            
            self.db.add(new_metrics)
            self.db.commit()
            
            logger.info(f"Quality metrics updated: trust={trust_score:.2f}, churn={churn_rate:.2%}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update metrics: {str(e)}")
            self.db.rollback()
            return False
