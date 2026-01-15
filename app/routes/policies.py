"""
Policies Routes
Policy recommendations page.
"""

from flask import Blueprint, render_template, jsonify, request
from app.services.mock_data import get_mock_policy_recommendations

policies_bp = Blueprint('policies', __name__)


@policies_bp.route('/')
def index():
    """Render the policies page."""
    return render_template('policies.html')


@policies_bp.route('/api/recommendations')
def get_recommendations():
    """Get policy recommendations."""
    try:
        severity = request.args.get('severity', None)
        
        recommendations = get_mock_policy_recommendations()
        
        # Filter by severity if provided
        if severity:
            recommendations = [r for r in recommendations if r['severity'] == severity]
        
        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': recommendations,
                'total': len(recommendations)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@policies_bp.route('/api/policy/<int:policy_id>')
def get_policy_detail(policy_id):
    """Get details for a specific policy."""
    try:
        recommendations = get_mock_policy_recommendations()
        policy = next((r for r in recommendations if r['id'] == policy_id), None)
        
        if not policy:
            return jsonify({
                'success': False,
                'error': 'Policy not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': policy
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
