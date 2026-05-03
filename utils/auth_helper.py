"""
Authentication helper functions
"""
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def guest_required(f):
    """Decorator to require guest user type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Access denied', 'error')
            return redirect(url_for('auth.login_page'))
        if session.get('role') != 'guest':
            flash('Access denied', 'error')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def host_required(f):
    """Decorator to require host user type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Access denied', 'error')
            return redirect(url_for('auth.login_page'))
        if session.get('role') != 'host':
            flash('Access denied', 'error')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin user type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and not restore_session_from_cookie():
            flash('Access denied', 'error')
            return redirect(url_for('auth.login_page'))
        if not session.get('is_admin', False):
            flash('Access denied - Admin privileges required', 'error')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function