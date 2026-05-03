"""
User model for SmartStay
"""
import bcrypt
import sqlite3
import pymysql
from database import get_db_connection, get_placeholder


def _resolve_row(row, key, index):
    """Return a row value for dict or tuple result."""
    if row is None:
        return None
    if isinstance(row, dict):
        return row.get(key)
    return row[index]


class User:
    def __init__(self, id=None, username=None, email=None, password=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at

    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(hashed_password, password):
        """Compare a plaintext password with a bcrypt hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def create(username, email, password):
        """Create and store a new user record with duplicate checking"""
        hashed_password = User.hash_password(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            # Check if username already exists
            cursor.execute(
                f'SELECT id FROM users WHERE username = {placeholder}',
                (username,)
            )
            if cursor.fetchone():
                return {
                    'success': False,
                    'error': 'Username already taken, please choose another one.'
                }

            # Check if email already exists
            cursor.execute(
                f'SELECT id FROM users WHERE email = {placeholder}',
                (email,)
            )
            if cursor.fetchone():
                return {
                    'success': False,
                    'error': 'Email already registered.'
                }

            # Insert new user
            cursor.execute(
                f'INSERT INTO users (username, email, password) VALUES ({placeholder}, {placeholder}, {placeholder})',
                (username, email, hashed_password)
            )
            conn.commit()
            user_id = cursor.lastrowid

            return {
                'success': True,
                'user': User(id=user_id, username=username, email=email)
            }

        except (sqlite3.IntegrityError, pymysql.IntegrityError) as e:
            conn.rollback()
            # Handle integrity constraint violations
            if 'username' in str(e).lower():
                return {
                    'success': False,
                    'error': 'Username already taken, please choose another one.'
                }
            elif 'email' in str(e).lower():
                return {
                    'success': False,
                    'error': 'Email already registered.'
                }
            else:
                return {
                    'success': False,
                    'error': 'An error occurred during registration. Please try again.'
                }
        except Exception as e:
            conn.rollback()
            return {
                'success': False,
                'error': 'An unexpected error occurred. Please try again later.'
            }
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_by_email(email):
        """Load a user by email."""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(
            f'SELECT id, username, email, password, created_at FROM users WHERE email = {placeholder}',
            (email,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            return None

        return User(
            id=_resolve_row(result, 'id', 0),
            username=_resolve_row(result, 'username', 1),
            email=_resolve_row(result, 'email', 2),
            password=_resolve_row(result, 'password', 3),
            created_at=_resolve_row(result, 'created_at', 4),
        )

    @staticmethod
    def find_by_username(username):
        """Load a user by username."""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(
            f'SELECT id, username, email, password, created_at FROM users WHERE username = {placeholder}',
            (username,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            return None

        return User(
            id=_resolve_row(result, 'id', 0),
            username=_resolve_row(result, 'username', 1),
            email=_resolve_row(result, 'email', 2),
            password=_resolve_row(result, 'password', 3),
            created_at=_resolve_row(result, 'created_at', 4),
        )

    @staticmethod
    def find_by_id(user_id):
        """Load a user by id."""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(
            f'SELECT id, username, email, password, created_at FROM users WHERE id = {placeholder}',
            (user_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            return None

        return User(
            id=_resolve_row(result, 'id', 0),
            username=_resolve_row(result, 'username', 1),
            email=_resolve_row(result, 'email', 2),
            password=_resolve_row(result, 'password', 3),
            created_at=_resolve_row(result, 'created_at', 4),
        )

    def to_dict(self):
        """Return a JSON-safe user representation."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
        }
