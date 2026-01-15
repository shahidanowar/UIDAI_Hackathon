"""
Prediction Routes
ML prediction page with risk assessment form.
"""

from flask import Blueprint, render_template, jsonify, request
from app.ml.model import get_prediction
from app.services.mock_data import get_mock_prediction

prediction_bp = Blueprint('prediction', __name__)


@prediction_bp.route('/')
def index():
    """Render the prediction page."""
    return render_template('prediction.html')


@prediction_bp.route('/api/predict', methods=['POST'])
def predict():
    """Make a risk prediction based on input features."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Validate required fields
        required_fields = ['state', 'records', 'anomalies']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {missing}'
            }), 400
        
        # Prepare features
        features = {
            'state': data.get('state'),
            'records': int(data.get('records', 0)),
            'anomalies': int(data.get('anomalies', 0)),
            'invalid_pin_rate': float(data.get('invalid_pin_rate', 0)),
            'duplicate_rate': float(data.get('duplicate_rate', 0)),
            'missing_dob_rate': float(data.get('missing_dob_rate', 0))
        }
        
        # Get prediction from ML model
        result = get_prediction(features)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid data format: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@prediction_bp.route('/api/states')
def get_states():
    """Get list of available states for the form."""
    states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Jammu and Kashmir"
    ]
    return jsonify({
        'success': True,
        'data': states
    })
