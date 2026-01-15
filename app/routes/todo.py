"""
To-Do Routes
Task management for anomaly resolution.
"""

from flask import Blueprint, render_template, jsonify, request
from app.extensions import db
from app.models import TodoTask
from app.services.mock_data import get_mock_tasks
from datetime import datetime

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/')
def index():
    """Render the to-do page."""
    return render_template('todo.html')


@todo_bp.route('/api/tasks')
def get_tasks():
    """Get all tasks with optional filtering."""
    status = request.args.get('status', None)
    priority = request.args.get('priority', None)
    state = request.args.get('state', None)
    
    try:
        # Try to get from database first
        query = TodoTask.query
        
        if status:
            query = query.filter(TodoTask.status == status)
        if priority:
            query = query.filter(TodoTask.priority == priority)
        if state:
            query = query.filter(TodoTask.state == state)
        
        tasks = query.order_by(TodoTask.created_at.desc()).all()
        
        if tasks:
            return jsonify({
                'success': True,
                'data': {
                    'tasks': [t.to_dict() for t in tasks],
                    'total': len(tasks)
                }
            })
        else:
            # Fall back to mock data if no database records
            mock_tasks = get_mock_tasks()
            
            # Apply filters to mock data
            if status:
                mock_tasks = [t for t in mock_tasks if t['status'] == status]
            if priority:
                mock_tasks = [t for t in mock_tasks if t['priority'] == priority]
            if state:
                mock_tasks = [t for t in mock_tasks if t['state'] == state]
            
            return jsonify({
                'success': True,
                'data': {
                    'tasks': mock_tasks,
                    'total': len(mock_tasks)
                }
            })
    except Exception as e:
        # If database error, use mock data
        mock_tasks = get_mock_tasks()
        return jsonify({
            'success': True,
            'data': {
                'tasks': mock_tasks,
                'total': len(mock_tasks)
            }
        })


@todo_bp.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Validate required fields
        if not data.get('title'):
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        task = TodoTask(
            title=data.get('title'),
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            state=data.get('state'),
            anomaly_type=data.get('anomaly_type'),
            assigned_to=data.get('assigned_to')
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todo_bp.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    """Update an existing task."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        task = TodoTask.query.get(task_id)
        
        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        # Update fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'state' in data:
            task.state = data['state']
        if 'anomaly_type' in data:
            task.anomaly_type = data['anomaly_type']
        if 'assigned_to' in data:
            task.assigned_to = data['assigned_to']
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': task.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todo_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    try:
        task = TodoTask.query.get(task_id)
        
        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todo_bp.route('/api/tasks/stats')
def get_task_stats():
    """Get task statistics."""
    try:
        tasks = get_mock_tasks()
        
        stats = {
            'total': len(tasks),
            'pending': len([t for t in tasks if t['status'] == 'pending']),
            'in_progress': len([t for t in tasks if t['status'] == 'in_progress']),
            'done': len([t for t in tasks if t['status'] == 'done']),
            'by_priority': {
                'critical': len([t for t in tasks if t['priority'] == 'critical']),
                'high': len([t for t in tasks if t['priority'] == 'high']),
                'medium': len([t for t in tasks if t['priority'] == 'medium']),
                'low': len([t for t in tasks if t['priority'] == 'low'])
            }
        }
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
