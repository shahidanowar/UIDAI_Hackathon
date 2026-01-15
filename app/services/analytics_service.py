"""
Analytics Service
Provides anomaly detection and statistical analysis.
"""

import os
import pandas as pd
from typing import Dict, List, Optional


class AnalyticsService:
    """Service for processing and analyzing Aadhaar data."""
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir
    
    def get_aggregated_stats_by_state(self, state: Optional[str] = None) -> List[Dict]:
        """Get aggregated statistics grouped by state."""
        # In production, this would query the database
        # For now, return empty list (mock data will be used)
        return []
    
    def detect_anomalies(self, data: pd.DataFrame) -> Dict:
        """Detect various anomalies in the dataset."""
        anomalies = {
            'duplicate_ids': [],
            'invalid_pincodes': [],
            'missing_dob': [],
            'invalid_phone': [],
            'impossible_age': [],
            'district_mismatch': [],
            'inconsistent_gender': []
        }
        
        # Duplicate detection
        if 'aadhaar_id' in data.columns:
            duplicates = data[data.duplicated(subset=['aadhaar_id'], keep=False)]
            anomalies['duplicate_ids'] = duplicates['aadhaar_id'].unique().tolist()[:100]
        
        # Invalid PIN codes (should be 6 digits)
        if 'pincode' in data.columns:
            invalid_pins = data[~data['pincode'].astype(str).str.match(r'^\d{6}$', na=False)]
            anomalies['invalid_pincodes'] = len(invalid_pins)
        
        # Missing DOB
        if 'dob' in data.columns:
            missing_dob = data[data['dob'].isna()]
            anomalies['missing_dob'] = len(missing_dob)
        
        return anomalies
    
    def calculate_correlation_warnings(self, data: pd.DataFrame) -> List[Dict]:
        """Calculate correlation between different anomaly types."""
        warnings = []
        # This would contain actual correlation logic in production
        return warnings
    
    def get_distribution_stats(self, data: pd.DataFrame) -> Dict:
        """Get distribution statistics for various fields."""
        stats = {
            'age_distribution': {},
            'gender_distribution': {},
            'state_distribution': {}
        }
        
        if 'age' in data.columns:
            age_bins = [0, 5, 18, 30, 45, 60, 150]
            age_labels = ['0-5', '5-17', '18-30', '31-45', '46-60', '60+']
            data['age_group'] = pd.cut(data['age'], bins=age_bins, labels=age_labels)
            stats['age_distribution'] = data['age_group'].value_counts().to_dict()
        
        if 'gender' in data.columns:
            stats['gender_distribution'] = data['gender'].value_counts().to_dict()
        
        if 'state' in data.columns:
            stats['state_distribution'] = data['state'].value_counts().to_dict()
        
        return stats


# Singleton instance
analytics_service = AnalyticsService()
