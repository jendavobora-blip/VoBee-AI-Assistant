"""
Marketing Intelligence Service
Advanced PR and marketing intelligence with dynamic product promotion
Includes dashboard rollback with owner approval priority
"""

from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class MarketingIntelligence:
    """
    Advanced marketing intelligence system for product promotion and analytics
    Supports mass-customized promotions and dynamic monitoring
    """
    
    def __init__(self):
        # Product catalog
        self.products = {}
        
        # Active promotions
        self.promotions = {}
        
        # Product bundles for mass customization
        self.bundles = {}
        
        # Analytics data
        self.analytics = {
            'total_promotions': 0,
            'active_promotions': 0,
            'total_conversions': 0,
            'revenue_generated': 0.0
        }
        
        # Dashboard changes requiring approval
        self.pending_approvals = {}
        
        # Approved dashboard configurations
        self.dashboard_configs = {}
        
        # Rollback history
        self.rollback_history = []
        
        logger.info("Marketing Intelligence Engine initialized")
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product in the catalog"""
        product_id = str(uuid.uuid4())
        product = {
            'id': product_id,
            'name': product_data.get('name'),
            'description': product_data.get('description'),
            'price': product_data.get('price'),
            'category': product_data.get('category'),
            'tags': product_data.get('tags', []),
            'created_at': datetime.utcnow().isoformat(),
            'status': 'active'
        }
        self.products[product_id] = product
        logger.info(f"Created product: {product_id} - {product['name']}")
        return product
    
    def create_promotion(self, promotion_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create dynamic product promotion
        Supports targeted, personalized, and mass promotions
        """
        promotion_id = str(uuid.uuid4())
        promotion = {
            'id': promotion_id,
            'name': promotion_data.get('name'),
            'description': promotion_data.get('description'),
            'product_ids': promotion_data.get('product_ids', []),
            'discount_percent': promotion_data.get('discount_percent', 0),
            'target_audience': promotion_data.get('target_audience', 'all'),
            'start_date': promotion_data.get('start_date', datetime.utcnow().isoformat()),
            'end_date': promotion_data.get('end_date'),
            'status': 'active',
            'conversions': 0,
            'revenue': 0.0,
            'created_at': datetime.utcnow().isoformat()
        }
        self.promotions[promotion_id] = promotion
        self.analytics['total_promotions'] += 1
        self.analytics['active_promotions'] += 1
        logger.info(f"Created promotion: {promotion_id} - {promotion['name']}")
        return promotion
    
    def create_bundle(self, bundle_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create product bundle for mass-customized promotion
        Enables L20 orchestration for advanced business products
        """
        bundle_id = str(uuid.uuid4())
        bundle = {
            'id': bundle_id,
            'name': bundle_data.get('name'),
            'description': bundle_data.get('description'),
            'product_ids': bundle_data.get('product_ids', []),
            'bundle_price': bundle_data.get('bundle_price'),
            'discount_percent': bundle_data.get('discount_percent', 0),
            'customization_options': bundle_data.get('customization_options', {}),
            'tier': bundle_data.get('tier', 'standard'),  # standard, premium, L20
            'status': 'active',
            'created_at': datetime.utcnow().isoformat()
        }
        self.bundles[bundle_id] = bundle
        logger.info(f"Created bundle: {bundle_id} - {bundle['name']} (Tier: {bundle['tier']})")
        return bundle
    
    def request_dashboard_change(self, change_data: Dict[str, Any], owner_id: str) -> Dict[str, Any]:
        """
        Request dashboard configuration change
        Requires owner approval before deployment
        """
        request_id = str(uuid.uuid4())
        change_request = {
            'id': request_id,
            'requested_by': change_data.get('requested_by'),
            'change_type': change_data.get('change_type'),  # config, layout, metrics
            'changes': change_data.get('changes'),
            'priority': change_data.get('priority', 'normal'),  # low, normal, high, critical
            'status': 'pending_approval',
            'owner_id': owner_id,
            'created_at': datetime.utcnow().isoformat(),
            'approved_at': None,
            'approved_by': None
        }
        self.pending_approvals[request_id] = change_request
        logger.info(f"Dashboard change requested: {request_id} (Priority: {change_request['priority']})")
        return change_request
    
    def approve_dashboard_change(self, request_id: str, approver_id: str) -> Dict[str, Any]:
        """
        Approve dashboard change request
        Owner approval priority system
        """
        if request_id not in self.pending_approvals:
            raise ValueError(f"Change request {request_id} not found")
        
        change_request = self.pending_approvals[request_id]
        
        # Verify approver has authority (owner)
        if approver_id != change_request['owner_id']:
            logger.warning(f"Unauthorized approval attempt by {approver_id}")
            raise PermissionError("Only owner can approve dashboard changes")
        
        # Save current config for rollback
        config_id = str(uuid.uuid4())
        if self.dashboard_configs:
            latest_config = list(self.dashboard_configs.values())[-1]
            self.rollback_history.append({
                'config_id': config_id,
                'previous_config': latest_config,
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Apply changes
        change_request['status'] = 'approved'
        change_request['approved_at'] = datetime.utcnow().isoformat()
        change_request['approved_by'] = approver_id
        
        # Create new dashboard config
        new_config = {
            'id': config_id,
            'changes_applied': change_request['changes'],
            'applied_at': datetime.utcnow().isoformat(),
            'request_id': request_id
        }
        self.dashboard_configs[config_id] = new_config
        
        # Move from pending to approved
        del self.pending_approvals[request_id]
        
        logger.info(f"Dashboard change approved: {request_id} by {approver_id}")
        return change_request
    
    def rollback_dashboard(self, config_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Rollback dashboard to previous configuration
        Owner approval priority
        """
        if not self.rollback_history:
            raise ValueError("No rollback history available")
        
        if config_id:
            # Rollback to specific config
            rollback_entry = next(
                (entry for entry in self.rollback_history if entry['config_id'] == config_id),
                None
            )
            if not rollback_entry:
                raise ValueError(f"Config {config_id} not found in rollback history")
        else:
            # Rollback to most recent
            rollback_entry = self.rollback_history[-1]
        
        # Apply rollback
        previous_config = rollback_entry['previous_config']
        rollback_config_id = str(uuid.uuid4())
        
        rollback_config = {
            'id': rollback_config_id,
            'changes_applied': previous_config['changes_applied'],
            'applied_at': datetime.utcnow().isoformat(),
            'rollback_from': rollback_entry['config_id'],
            'rollback_timestamp': datetime.utcnow().isoformat()
        }
        
        self.dashboard_configs[rollback_config_id] = rollback_config
        
        logger.info(f"Dashboard rolled back to config: {rollback_entry['config_id']}")
        return rollback_config
    
    def get_analytics(self, timeframe: str = '30d') -> Dict[str, Any]:
        """Get marketing analytics for specified timeframe"""
        return {
            **self.analytics,
            'timeframe': timeframe,
            'total_products': len(self.products),
            'total_bundles': len(self.bundles),
            'active_promotions': self.analytics['active_promotions'],
            'pending_approvals': len(self.pending_approvals),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_promotion_performance(self, promotion_id: str) -> Dict[str, Any]:
        """Get detailed performance metrics for a promotion"""
        if promotion_id not in self.promotions:
            raise ValueError(f"Promotion {promotion_id} not found")
        
        promotion = self.promotions[promotion_id]
        
        return {
            'promotion_id': promotion_id,
            'name': promotion['name'],
            'conversions': promotion['conversions'],
            'revenue': promotion['revenue'],
            'discount_percent': promotion['discount_percent'],
            'roi': self._calculate_roi(promotion),
            'status': promotion['status'],
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _calculate_roi(self, promotion: Dict[str, Any]) -> float:
        """Calculate ROI for a promotion"""
        # Simplified ROI calculation
        if promotion['revenue'] == 0:
            return 0.0
        # Assuming 20% cost of promotion
        cost = promotion['revenue'] * 0.20
        return round((promotion['revenue'] - cost) / cost * 100, 2)

# Initialize marketing intelligence
marketing = MarketingIntelligence()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "marketing-intelligence",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/products', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        product = marketing.create_product(data)
        return jsonify(product), 201
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/products', methods=['GET'])
def list_products():
    """List all products"""
    return jsonify({
        "products": list(marketing.products.values()),
        "total": len(marketing.products)
    })

@app.route('/promotions', methods=['POST'])
def create_promotion():
    """Create a new promotion"""
    try:
        data = request.get_json()
        promotion = marketing.create_promotion(data)
        return jsonify(promotion), 201
    except Exception as e:
        logger.error(f"Error creating promotion: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/promotions', methods=['GET'])
def list_promotions():
    """List all active promotions"""
    active_promotions = [p for p in marketing.promotions.values() if p['status'] == 'active']
    return jsonify({
        "promotions": active_promotions,
        "total": len(active_promotions)
    })

@app.route('/promotions/<promotion_id>/performance', methods=['GET'])
def get_promotion_performance(promotion_id):
    """Get promotion performance metrics"""
    try:
        performance = marketing.get_promotion_performance(promotion_id)
        return jsonify(performance)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error getting promotion performance: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bundles', methods=['POST'])
def create_bundle():
    """Create a product bundle"""
    try:
        data = request.get_json()
        bundle = marketing.create_bundle(data)
        return jsonify(bundle), 201
    except Exception as e:
        logger.error(f"Error creating bundle: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bundles', methods=['GET'])
def list_bundles():
    """List all product bundles"""
    return jsonify({
        "bundles": list(marketing.bundles.values()),
        "total": len(marketing.bundles)
    })

@app.route('/dashboard/change-request', methods=['POST'])
def request_dashboard_change():
    """Request dashboard configuration change"""
    try:
        data = request.get_json()
        owner_id = data.get('owner_id')
        
        if not owner_id:
            return jsonify({"error": "owner_id is required"}), 400
        
        change_request = marketing.request_dashboard_change(data, owner_id)
        return jsonify(change_request), 201
    except Exception as e:
        logger.error(f"Error requesting dashboard change: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard/approve/<request_id>', methods=['POST'])
def approve_dashboard_change(request_id):
    """Approve dashboard change request (owner only)"""
    try:
        data = request.get_json()
        approver_id = data.get('approver_id')
        
        if not approver_id:
            return jsonify({"error": "approver_id is required"}), 400
        
        result = marketing.approve_dashboard_change(request_id, approver_id)
        return jsonify(result)
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error approving dashboard change: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard/rollback', methods=['POST'])
def rollback_dashboard():
    """Rollback dashboard to previous configuration"""
    try:
        data = request.get_json()
        config_id = data.get('config_id') if data else None
        
        result = marketing.rollback_dashboard(config_id)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error rolling back dashboard: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard/pending-approvals', methods=['GET'])
def get_pending_approvals():
    """Get all pending dashboard change approvals"""
    return jsonify({
        "pending_approvals": list(marketing.pending_approvals.values()),
        "total": len(marketing.pending_approvals)
    })

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get marketing analytics"""
    timeframe = request.args.get('timeframe', '30d')
    analytics = marketing.get_analytics(timeframe)
    return jsonify(analytics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=False)
