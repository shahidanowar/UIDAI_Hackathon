"""
Database Models
"""

from datetime import datetime
from app.extensions import db


class TodoTask(db.Model):
    """Model for anomaly verification tasks."""
    __tablename__ = 'todo_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, done
    priority = db.Column(db.String(50), default='medium')  # low, medium, high
    state = db.Column(db.String(100))
    anomaly_type = db.Column(db.String(100))
    assigned_to = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'state': self.state,
            'anomaly_type': self.anomaly_type,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AnomalyLog(db.Model):
    """Model for logging detected anomalies."""
    __tablename__ = 'anomaly_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100))
    anomaly_type = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(50))  # low, medium, high, critical
    count = db.Column(db.Integer, default=1)
    details = db.Column(db.Text)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'district': self.district,
            'anomaly_type': self.anomaly_type,
            'severity': self.severity,
            'count': self.count,
            'details': self.details,
            'detected_at': self.detected_at.isoformat() if self.detected_at else None,
            'resolved': self.resolved,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }


class StateStats(db.Model):
    """Aggregated state statistics for fast dashboard queries."""
    __tablename__ = 'state_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False, unique=True)
    total_records = db.Column(db.Integer, default=0)
    total_anomalies = db.Column(db.Integer, default=0)
    anomaly_rate = db.Column(db.Float, default=0.0)
    invalid_pin_count = db.Column(db.Integer, default=0)
    duplicate_count = db.Column(db.Integer, default=0)
    missing_dob_count = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'total_records': self.total_records,
            'total_anomalies': self.total_anomalies,
            'anomaly_rate': self.anomaly_rate,
            'invalid_pin_count': self.invalid_pin_count,
            'duplicate_count': self.duplicate_count,
            'missing_dob_count': self.missing_dob_count,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
