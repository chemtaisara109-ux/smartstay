"""
Advanced Authentication Service for SmartStay
Handles password reset, remember me, and token management
"""
import secrets
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from flask import session, redirect, url_for, flash, request
from models.user_enhanced import User
from database import get_db_connection, get_placeholder

class PasswordResetToken:
    """Manage password reset tokens"""
    
    @staticmethod
    def generate_token():
        """Generate a secure reset token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def create_reset_token(email):
        """Create a password reset token for user"""
        user = User.find_by_email(email)
        if not user:
            return None
        
        token = PasswordResetToken.generate_token()
        expires_at = (datetime.utcnow() + timedelta(hours=24)).isoformat(sep=' ')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()
        
        try:
            cursor.execute(f'''
                INSERT INTO password_resets (user_id, token, expires_at)
                VALUES ({placeholder}, {placeholder}, {placeholder})
            ''', (user.id, token, expires_at))
            conn.commit()
            return token
        except Exception as e:
            conn.rollback()
            print(f"Error creating reset token: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def verify_reset_token(token):
        """Verify and get user from reset token"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()
        
        try:
            cursor.execute(f'''
                SELECT user_id FROM password_resets
                WHERE token = {placeholder}
                AND expires_at > CURRENT_TIMESTAMP
                AND used = FALSE
            ''', (token,))
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                user_id = result[0] if isinstance(result, tuple) else result.get('user_id')
                return User.find_by_id(user_id)
            return None
        except Exception as e:
            print(f"Error verifying reset token: {e}")
            return None
    
    @staticmethod
    def mark_token_used(token):
        """Mark token as used"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()
        
        try:
            cursor.execute(f'''
                UPDATE password_resets
                SET used = TRUE
                WHERE token = {placeholder}
            ''', (token,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error marking token used: {e}")
        finally:
            cursor.close()
            conn.close()


class RememberMe:
    """Manage Remember Me functionality"""
    
    @staticmethod
    def create_remember_token(user_id):
        """Create a remember me token"""
        token = secrets.token_urlsafe(32)
        expires_at = (datetime.utcnow() + timedelta(days=30)).isoformat(sep=' ')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()
        
        try:
            cursor.execute(f'''
                INSERT INTO remember_tokens (user_id, token, expires_at)
                VALUES ({placeholder}, {placeholder}, {placeholder})
            ''', (user_id, token, expires_at))
            conn.commit()
            return token
        except Exception as e:
            conn.rollback()
            print(f"Error creating remember token: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def verify_remember_token(token):
        """Verify remember me token"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()
        
        try:
            cursor.execute(f'''
                SELECT user_id FROM remember_tokens
                WHERE token = {placeholder}
                AND expires_at > CURRENT_TIMESTAMP
            ''', (token,))
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                user_id = result[0] if isinstance(result, tuple) else result.get('user_id')
                return user_id
            return None
        except Exception as e:
            print(f"Error verifying remember token: {e}")
            return None


def restore_session_from_cookie():
    """Restore user session from remember-me cookie if available"""
    if 'user_id' in session:
        return True

    remember_token = request.cookies.get('remember_token')
    if not remember_token:
        return False

    user_id = RememberMe.verify_remember_token(remember_token)
    if not user_id:
        return False

    user = User.find_by_id(user_id)
    if not user:
        return False

    session['user_id'] = user.id
    session['username'] = user.username
    session['full_name'] = user.full_name
    session['email'] = user.email
    session['role'] = user.role
    session.permanent = True
    return True


def auto_login_from_cookie(f):
    """Decorator to auto-login user from remember me cookie"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        restore_session_from_cookie()
        return f(*args, **kwargs)
    return decorated_function
