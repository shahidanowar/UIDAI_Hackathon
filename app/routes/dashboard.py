"""
Dashboard Routes
Main dashboard page with India map and summary statistics.
"""

from flask import Blueprint, render_template, jsonify, request
from app.services.mock_data import (
    get_mock_dashboard_summary,
    get_mock_state_data,
    get_mock_all_states_data
)

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('dashboard.html')


@dashboard_bp.route('/api/dashboard/summary')
def get_summary():
    """Get dashboard summary statistics."""
    try:
        # In production, this would query the database
        # For now, use mock data
        data = get_mock_dashboard_summary()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_bp.route('/api/dashboard/states')
def get_all_states():
    """Get data for all states (for map coloring)."""
    try:
        data = get_mock_all_states_data()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_bp.route('/api/dashboard/state')
def get_state_data():
    """Get detailed data for a specific state."""
    state = request.args.get('state', '')
    
    if not state:
        return jsonify({
            'success': False,
            'error': 'State parameter is required'
        }), 400
    
    try:
        data = get_mock_state_data(state)
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_bp.route('/api/dashboard/state/districts')
def get_state_districts():
    """Get district-level data for a specific state."""
    state = request.args.get('state', '')
    
    if not state:
        return jsonify({
            'success': False,
            'error': 'State parameter is required'
        }), 400
    
    try:
        data = get_mock_state_data(state)
        return jsonify({
            'success': True,
            'data': {
                'state': state,
                'districts': data.get('district_distribution', [])
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
