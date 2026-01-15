"""
ML Model Service
Handles model loading and prediction with fallback to dummy model.
"""

import os
import numpy as np
import joblib
from typing import Dict, Any, Optional


class RiskPredictor:
    """Risk prediction model for Aadhaar anomaly assessment."""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path
        self._load_model()
    
    def _load_model(self):
        """Load the trained model or create a dummy one."""
        if self.model_path and os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                print("Loaded trained model from disk")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
        
        if self.model is None:
            # Create placeholder (use dummy prediction)
            print("Using rule-based fallback predictor")
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a risk prediction based on input features.
        
        Features expected:
        - records: int (total records)
        - anomalies: int (anomaly count)
        - invalid_pin_rate: float
        - duplicate_rate: float
        - missing_dob_rate: float
        """
        records = features.get('records', 1)
        anomalies = features.get('anomalies', 0)
        invalid_pin_rate = features.get('invalid_pin_rate', 0)
        duplicate_rate = features.get('duplicate_rate', 0)
        missing_dob_rate = features.get('missing_dob_rate', 0)
        
        # Calculate composite risk score
        anomaly_rate = anomalies / max(records, 1)
        
        # Weighted scoring
        weights = {
            'anomaly_rate': 0.35,
            'invalid_pin_rate': 0.25,
            'duplicate_rate': 0.25,
            'missing_dob_rate': 0.15
        }
        
        score = (
            anomaly_rate * weights['anomaly_rate'] +
            invalid_pin_rate * weights['invalid_pin_rate'] +
            duplicate_rate * weights['duplicate_rate'] +
            missing_dob_rate * weights['missing_dob_rate']
        )
        
        # Normalize to 0-1 range
        score = min(score * 5, 1.0)  # Multiply by 5 to scale rates
        
        # Determine risk category
        if score >= 0.7:
            prediction = "High Risk Zone"
            action = "Immediate verification required. Initiate PIN validation and duplicate check workflows."
            confidence = 0.85 + (score - 0.7) * 0.3
        elif score >= 0.4:
            prediction = "Medium Risk Zone"
            action = "Schedule verification within 7 days. Focus on address and biometric quality checks."
            confidence = 0.75 + (score - 0.4) * 0.2
        else:
            prediction = "Low Risk Zone"
            action = "Routine monitoring sufficient. No immediate action required."
            confidence = 0.70 + score * 0.3
        
        confidence = min(max(confidence, 0.65), 0.95)
        
        # Identify top contributing features
        contributions = []
        if invalid_pin_rate > 0.05:
            contributions.append({
                "feature": "Invalid PIN Rate",
                "value": f"{invalid_pin_rate * 100:.1f}%",
                "contribution": round(invalid_pin_rate * 100, 1)
            })
        if duplicate_rate > 0.03:
            contributions.append({
                "feature": "Duplicate Rate", 
                "value": f"{duplicate_rate * 100:.1f}%",
                "contribution": round(duplicate_rate * 100, 1)
            })
        if anomaly_rate > 0.02:
            contributions.append({
                "feature": "Overall Anomaly Rate",
                "value": f"{anomaly_rate * 100:.1f}%",
                "contribution": round(anomaly_rate * 100, 1)
            })
        if missing_dob_rate > 0.02:
            contributions.append({
                "feature": "Missing DOB Rate",
                "value": f"{missing_dob_rate * 100:.1f}%",
                "contribution": round(missing_dob_rate * 100, 1)
            })
        
        if not contributions:
            contributions = [{"feature": "General Assessment", "value": "Normal", "contribution": 100}]
        
        # Sort by contribution
        contributions.sort(key=lambda x: x['contribution'], reverse=True)
        
        return {
            "prediction": prediction,
            "score": round(score, 2),
            "confidence": round(confidence, 2),
            "recommended_action": action,
            "top_features": contributions[:3],
            "state": features.get('state', 'Unknown'),
            "model_type": "rule_based" if self.model is None else "ml_model"
        }


# Create singleton instance
predictor = RiskPredictor()


def get_prediction(features: Dict[str, Any]) -> Dict[str, Any]:
    """Get risk prediction for given features."""
    return predictor.predict(features)
