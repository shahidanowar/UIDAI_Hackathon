"""
Analysis Routes
Analysis page with anomaly detection and statistical patterns.
"""

from flask import Blueprint, render_template, jsonify, request
from app.services.mock_data import get_mock_analysis_report

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/')
def index():
    """Render the analysis page."""
    return render_template('analysis.html')


@analysis_bp.route('/api/report')
def get_report():
    """Get full analysis report."""
    try:
        data = get_mock_analysis_report()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analysis_bp.route('/api/anomalies')
def get_anomalies():
    """Get filtered anomalies."""
    state = request.args.get('state', None)
    anomaly_type = request.args.get('type', None)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    try:
        report = get_mock_analysis_report()
        anomalies = report.get('anomaly_frequency', [])
        
        # Filter by state if provided
        if state:
            # In production, would filter by state
            pass
        
        # Filter by type if provided
        if anomaly_type:
            anomalies = [a for a in anomalies if a['type'] == anomaly_type]
        
        # Paginate
        start = (page - 1) * per_page
        end = start + per_page
        paginated = anomalies[start:end]
        
        return jsonify({
            'success': True,
            'data': {
                'anomalies': paginated,
                'total': len(anomalies),
                'page': page,
                'per_page': per_page,
                'total_pages': (len(anomalies) + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analysis_bp.route('/api/distributions')
def get_distributions():
    """Get distribution data for charts."""
    try:
        report = get_mock_analysis_report()
        return jsonify({
            'success': True,
            'data': {
                'age_distribution': report.get('age_distribution', {}),
                'gender_distribution': report.get('gender_distribution', {})
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
