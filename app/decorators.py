from functools import wraps
from flask import session, flash, redirect, url_for
from app import db
from app.models.user import User

def login_required(f):
    """Decorator to require login for user routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def approved_required(f):
    """Decorator to require both login and approved status for user routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        
        # Check if user is approved
        user = db.session.get(User, session['user_id'])
        if not user:
            session.clear()
            flash('User account not found', 'danger')
            return redirect(url_for('login'))
        
        if user.status != 'approved':
            flash('Your account is pending approval. Please wait for admin verification.', 'warning')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        
        user = db.session.get(User, session['user_id'])
        if not user or user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function
