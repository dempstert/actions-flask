"""Application routes."""
from flask import Blueprint, jsonify, request
from app import db
from app.models import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home endpoint."""
    return jsonify({
        'message': 'Welcome to Flask App',
        'status': 'running'
    })


@main_bp.route('/health')
def health():
    """Health check endpoint."""
    try:
        # Check database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


@main_bp.route('/users', methods=['GET', 'POST'])
def users():
    """Get all users or create a new user."""
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({'error': 'Missing username or email'}), 400
        
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201
    
    # GET request
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@main_bp.route('/users/<int:user_id>')
def get_user(user_id):
    """Get a specific user."""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())
