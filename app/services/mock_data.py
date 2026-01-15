"""
Mock Data Service
Generates realistic mock data for all endpoints when database is not populated.
"""

import random
from datetime import datetime, timedelta

# Indian states with realistic data
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Jammu and Kashmir"
]

DISTRICTS_BY_STATE = {
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Allahabad", "Gorakhpur", "Meerut", "Ghaziabad"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur", "Kolhapur"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Begusarai", "Munger"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Bardhaman", "Malda", "Hooghly"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Tirupati", "Kakinada", "Chittoor"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Erode", "Vellore"],
    "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum", "Gulbarga", "Davangere", "Bellary"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Junagadh", "Gandhinagar"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner", "Ajmer", "Bhilwara", "Alwar"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Palakkad", "Kannur", "Malappuram"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain", "Sagar", "Dewas", "Satna"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Ramagundam", "Mahbubnagar", "Nalgonda"],
    "Delhi": ["Central Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi", "New Delhi", "North West Delhi", "South West Delhi"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia", "Tezpur", "Bongaigaon"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Pathankot", "Hoshiarpur"],
}

ANOMALY_TYPES = [
    "Duplicate Aadhaar ID",
    "Invalid PIN Code",
    "Missing DOB",
    "Invalid Phone Format",
    "Impossible Age (0 or 150+)",
    "District-State Mismatch",
    "Inconsistent Gender Labels",
    "Biometric Quality Issues",
    "Address Format Errors",
    "Name Character Issues"
]


def get_mock_dashboard_summary():
    """Generate mock dashboard summary data."""
    total_records = random.randint(4500000, 5500000)
    total_anomalies = random.randint(150000, 300000)
    verified_fixed = random.randint(50000, 100000)
    
    # Most affected states
    affected_states = random.sample(INDIAN_STATES, 5)
    most_affected = [
        {"state": state, "anomaly_count": random.randint(10000, 50000)}
        for state in affected_states
    ]
    most_affected.sort(key=lambda x: x["anomaly_count"], reverse=True)
    
    return {
        "total_records": total_records,
        "total_anomalies": total_anomalies,
        "anomaly_rate": round(total_anomalies / total_records * 100, 2),
        "verified_fixed": verified_fixed,
        "pending_verification": total_anomalies - verified_fixed,
        "most_affected_states": most_affected,
        "last_updated": datetime.now().isoformat()
    }


def get_mock_state_data(state_name):
    """Generate mock data for a specific state."""
    total_records = random.randint(100000, 500000)
    total_anomalies = random.randint(5000, 50000)
    
    # Get districts for this state
    districts = DISTRICTS_BY_STATE.get(state_name, ["District 1", "District 2", "District 3"])
    
    # Top anomaly types
    top_anomalies = random.sample(ANOMALY_TYPES, 3)
    anomaly_breakdown = [
        {"type": anomaly, "count": random.randint(1000, 10000)}
        for anomaly in top_anomalies
    ]
    anomaly_breakdown.sort(key=lambda x: x["count"], reverse=True)
    
    # District distribution
    district_data = [
        {"district": district, "records": random.randint(10000, 80000), "anomalies": random.randint(500, 5000)}
        for district in districts[:6]
    ]
    
    return {
        "state": state_name,
        "total_records": total_records,
        "total_anomalies": total_anomalies,
        "anomaly_rate": round(total_anomalies / total_records * 100, 2),
        "top_anomaly_types": anomaly_breakdown,
        "district_distribution": district_data,
        "invalid_pin_rate": round(random.uniform(0.02, 0.15), 3),
        "duplicate_rate": round(random.uniform(0.01, 0.08), 3),
        "missing_dob_rate": round(random.uniform(0.01, 0.05), 3)
    }


def get_mock_all_states_data():
    """Generate mock data for all states (for map coloring)."""
    states_data = []
    for state in INDIAN_STATES:
        total_records = random.randint(50000, 600000)
        total_anomalies = random.randint(2000, 60000)
        states_data.append({
            "state": state,
            "total_records": total_records,
            "total_anomalies": total_anomalies,
            "anomaly_rate": round(total_anomalies / total_records * 100, 2),
            "severity": "high" if total_anomalies > 40000 else "medium" if total_anomalies > 15000 else "low"
        })
    return states_data


def get_mock_analysis_report():
    """Generate mock analysis report data."""
    # Age distribution
    age_distribution = {
        "0-5": random.randint(200000, 400000),
        "5-17": random.randint(800000, 1200000),
        "18-30": random.randint(1000000, 1500000),
        "31-45": random.randint(800000, 1200000),
        "46-60": random.randint(500000, 800000),
        "60+": random.randint(300000, 500000)
    }
    
    # Gender distribution
    gender_distribution = {
        "Male": random.randint(2500000, 2800000),
        "Female": random.randint(2200000, 2600000),
        "Other": random.randint(5000, 15000),
        "Not Specified": random.randint(10000, 30000)
    }
    
    # Anomaly frequency
    anomaly_frequency = [
        {"type": anomaly, "count": random.randint(5000, 80000)}
        for anomaly in ANOMALY_TYPES
    ]
    anomaly_frequency.sort(key=lambda x: x["count"], reverse=True)
    
    # Correlation warnings
    correlation_warnings = [
        {
            "warning": "High correlation between Invalid PIN Code and District-State Mismatch",
            "correlation": 0.87,
            "severity": "high"
        },
        {
            "warning": "Missing DOB often occurs with Biometric Quality Issues",
            "correlation": 0.65,
            "severity": "medium"
        },
        {
            "warning": "Duplicate records cluster in urban districts",
            "correlation": 0.72,
            "severity": "medium"
        },
        {
            "warning": "Impossible Age values linked with Name Character Issues",
            "correlation": 0.45,
            "severity": "low"
        }
    ]
    
    # State-wise anomaly distribution
    state_anomaly_distribution = [
        {"state": state, "anomalies": random.randint(5000, 50000)}
        for state in random.sample(INDIAN_STATES, 10)
    ]
    state_anomaly_distribution.sort(key=lambda x: x["anomalies"], reverse=True)
    
    # Suspicious patterns
    suspicious_patterns = [
        {
            "pattern": "Bulk enrollments with sequential Aadhaar IDs detected in Bihar",
            "affected_records": random.randint(1000, 5000),
            "risk_level": "critical"
        },
        {
            "pattern": "Unusual spike in biometric rejections in Mumbai (Nov 2025)",
            "affected_records": random.randint(500, 2000),
            "risk_level": "high"
        },
        {
            "pattern": "Same mobile number linked to 50+ Aadhaar records in Delhi",
            "affected_records": random.randint(100, 500),
            "risk_level": "critical"
        },
        {
            "pattern": "Address field contains PO Box patterns (potential fraud)",
            "affected_records": random.randint(200, 800),
            "risk_level": "medium"
        }
    ]
    
    return {
        "age_distribution": age_distribution,
        "gender_distribution": gender_distribution,
        "anomaly_frequency": anomaly_frequency,
        "correlation_warnings": correlation_warnings,
        "state_anomaly_distribution": state_anomaly_distribution,
        "suspicious_patterns": suspicious_patterns,
        "total_records_analyzed": random.randint(4500000, 5500000),
        "analysis_date": datetime.now().isoformat()
    }


def get_mock_prediction(data):
    """Generate mock prediction response."""
    # Calculate risk score based on input
    anomaly_rate = data.get('anomalies', 0) / max(data.get('records', 1), 1)
    invalid_pin_rate = data.get('invalid_pin_rate', 0)
    duplicate_rate = data.get('duplicate_rate', 0)
    
    # Simple scoring logic
    score = anomaly_rate * 0.4 + invalid_pin_rate * 0.3 + duplicate_rate * 0.3
    score = min(score * 3, 1.0)  # Normalize
    
    # Add some randomness for demo
    score = score * 0.7 + random.uniform(0.1, 0.3)
    score = min(max(score, 0.1), 0.95)
    
    if score >= 0.7:
        prediction = "High Risk Zone"
        action = "Immediate verification required. Initiate PIN validation and duplicate check workflows."
    elif score >= 0.4:
        prediction = "Medium Risk Zone"
        action = "Schedule verification within 7 days. Focus on address and biometric quality checks."
    else:
        prediction = "Low Risk Zone"
        action = "Routine monitoring sufficient. No immediate action required."
    
    # Top contributing features
    features = []
    if invalid_pin_rate > 0.1:
        features.append({"feature": "Invalid PIN Rate", "contribution": round(invalid_pin_rate * 100, 1)})
    if duplicate_rate > 0.05:
        features.append({"feature": "Duplicate Rate", "contribution": round(duplicate_rate * 100, 1)})
    if anomaly_rate > 0.03:
        features.append({"feature": "Overall Anomaly Rate", "contribution": round(anomaly_rate * 100, 1)})
    
    return {
        "prediction": prediction,
        "score": round(score, 2),
        "confidence": round(random.uniform(0.75, 0.95), 2),
        "recommended_action": action,
        "top_features": features if features else [{"feature": "General Assessment", "contribution": 100}],
        "state": data.get('state', 'Unknown')
    }


def get_mock_policy_recommendations():
    """Generate mock policy recommendations."""
    return [
        {
            "id": 1,
            "title": "PIN Code Validation & Correction",
            "severity": "critical",
            "reason": "12.5% of records have invalid PIN codes that don't match state/district mapping",
            "steps": [
                "Export all records with PIN code mismatches",
                "Cross-reference with India Post PIN database",
                "Generate correction candidates using fuzzy matching",
                "Queue corrected records for operator verification",
                "Update database after manual approval"
            ],
            "executor": "System + Operator",
            "expected_outcome": "95% PIN code accuracy improvement",
            "estimated_impact": 625000
        },
        {
            "id": 2,
            "title": "Duplicate Aadhaar ID Resolution",
            "severity": "critical",
            "reason": "6.2% records flagged as potential duplicates based on biometric similarity",
            "steps": [
                "Run biometric matching algorithm on flagged records",
                "Generate duplicate pairs with similarity scores",
                "Present to verification team for manual review",
                "Merge/invalidate confirmed duplicates",
                "Generate audit trail for compliance"
            ],
            "executor": "Admin + Verification Team",
            "expected_outcome": "Eliminate duplicate entries, improve data integrity",
            "estimated_impact": 310000
        },
        {
            "id": 3,
            "title": "Mobile OTP Re-confirmation",
            "severity": "high",
            "reason": "3.8% of records have invalid phone formats or multiple Aadhaar linked to same number",
            "steps": [
                "Identify all records with phone format issues",
                "Send OTP to registered numbers for re-verification",
                "Mark non-responsive records for manual outreach",
                "Update phone numbers post verification",
                "Generate compliance report"
            ],
            "executor": "System + Call Center",
            "expected_outcome": "Valid phone linkage for 98% records",
            "estimated_impact": 190000
        },
        {
            "id": 4,
            "title": "DOB Missing/Invalid Correction",
            "severity": "high",
            "reason": "2.1% records have missing or impossible DOB values",
            "steps": [
                "Extract records with DOB issues",
                "Cross-reference with enrollment documents",
                "Request document re-submission where needed",
                "Apply age validation rules",
                "Update corrected DOB values"
            ],
            "executor": "Operator",
            "expected_outcome": "Complete DOB coverage with validation",
            "estimated_impact": 105000
        },
        {
            "id": 5,
            "title": "District-State Mapping Correction",
            "severity": "medium",
            "reason": "1.5% records have district names not matching their assigned states",
            "steps": [
                "Run district-state validation check",
                "Generate list of mismatched records",
                "Use address parsing to determine correct mapping",
                "Apply bulk corrections for high-confidence matches",
                "Queue ambiguous cases for manual review"
            ],
            "executor": "System + Operator",
            "expected_outcome": "100% correct district-state mapping",
            "estimated_impact": 75000
        },
        {
            "id": 6,
            "title": "Biometric Quality Enhancement",
            "severity": "medium",
            "reason": "0.8% records have low-quality biometric data",
            "steps": [
                "Identify records with quality scores below threshold",
                "Prioritize by enrollment date and usage frequency",
                "Schedule re-enrollment camps",
                "Track re-enrollment completion",
                "Update quality metrics"
            ],
            "executor": "Field Team + Admin",
            "expected_outcome": "Biometric quality score above 80% for all records",
            "estimated_impact": 40000
        }
    ]


def get_mock_tasks():
    """Generate mock to-do tasks."""
    tasks = [
        {
            "id": 1,
            "title": "Verify duplicate Aadhaar IDs in Assam",
            "description": "Review 1,247 potential duplicate records flagged by biometric matching",
            "status": "in_progress",
            "priority": "high",
            "state": "Assam",
            "anomaly_type": "Duplicate Aadhaar ID",
            "assigned_to": "Verification Team A",
            "created_at": (datetime.now() - timedelta(days=3)).isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "id": 2,
            "title": "Cross-check PIN mismatch in West Bengal",
            "description": "Validate 3,890 records with PIN codes not matching district mapping",
            "status": "pending",
            "priority": "high",
            "state": "West Bengal",
            "anomaly_type": "Invalid PIN Code",
            "assigned_to": "Data Quality Team",
            "created_at": (datetime.now() - timedelta(days=5)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=1)).isoformat()
        },
        {
            "id": 3,
            "title": "Revalidate DOB missing cases in Bihar",
            "description": "Process 892 records with missing date of birth",
            "status": "pending",
            "priority": "medium",
            "state": "Bihar",
            "anomaly_type": "Missing DOB",
            "assigned_to": "Enrollment Center",
            "created_at": (datetime.now() - timedelta(days=7)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=7)).isoformat()
        },
        {
            "id": 4,
            "title": "Manual verification - suspicious bulk enrollments",
            "description": "Investigate 234 sequential Aadhaar IDs enrolled on same day at Patna center",
            "status": "in_progress",
            "priority": "critical",
            "state": "Bihar",
            "anomaly_type": "Suspicious Pattern",
            "assigned_to": "Fraud Investigation Unit",
            "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "id": 5,
            "title": "Resolve mobile number conflicts in Delhi",
            "description": "Process 567 cases where single mobile linked to multiple Aadhaar",
            "status": "done",
            "priority": "high",
            "state": "Delhi",
            "anomaly_type": "Invalid Phone Format",
            "assigned_to": "Call Center Team",
            "created_at": (datetime.now() - timedelta(days=10)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=2)).isoformat()
        },
        {
            "id": 6,
            "title": "Update biometric quality scores - Maharashtra",
            "description": "Re-enroll 1,450 records with low biometric quality",
            "status": "pending",
            "priority": "low",
            "state": "Maharashtra",
            "anomaly_type": "Biometric Quality Issues",
            "assigned_to": "Field Team B",
            "created_at": (datetime.now() - timedelta(days=14)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=14)).isoformat()
        }
    ]
    return tasks
