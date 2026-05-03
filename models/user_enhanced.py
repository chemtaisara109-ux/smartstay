"""
Enhanced User model for SmartStay with role-based fields
"""
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, get_placeholder


class User:
    def __init__(self, id=None, username=None, full_name=None, email=None, password=None, 
                 role='guest', phone=None, property_name=None, location=None, created_at=None, **kwargs):
        self.id = id
        self.username = username
        self.full_name = full_name
        self.email = email
        self.password = password
        self.role = role or 'guest'
        self.phone = phone
        self.property_name = property_name
        self.location = location
        self.created_at = created_at
        
        # Store additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def hash_password(password):
        """Hash password using Werkzeug security"""
        return generate_password_hash(password)

    @staticmethod
    def check_password(hashed_password, password):
        """Compare a plaintext password with a secure hash"""
        try:
            return check_password_hash(hashed_password, password)
        except Exception as e:
            print(f"Password verification error: {e}")
            return False

    @staticmethod
    def create(username, full_name, email, password, role='guest', phone=None, 
               property_name=None, location=None):
        """Create and store a new user record"""
        email = email.strip().lower()
        hashed_password = User.hash_password(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            if role == 'host':
                cursor.execute(f'''
                    INSERT INTO users (username, full_name, email, password, role, phone, property_name, location)
                    VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
                ''', (username, full_name, email, hashed_password, role, phone, property_name, location))
            else:
                cursor.execute(f'''
                    INSERT INTO users (username, full_name, email, password, role)
                    VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
                ''', (username, full_name, email, hashed_password, role))
            
            # Always commit the transaction
            conn.commit()
            
            user_id = cursor.lastrowid
            return User(id=user_id, username=username, full_name=full_name, email=email, role=role)
        except Exception as e:
            conn.rollback()
            print(f"Error creating user: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    def find_by_email(email):
        """Load a user by email."""
        email = email.strip().lower()
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(f'''
                SELECT id, username, full_name, email, password, role, phone, property_name, location, created_at
                FROM users WHERE LOWER(email) = LOWER({placeholder})
            ''', (email,))
            
            result = cursor.fetchone()
            
            if not result:
                return None

            # Handle both dict and tuple results
            if isinstance(result, dict):
                return User(
                    id=result.get('id'),
                    username=result.get('username'),
                    full_name=result.get('full_name'),
                    email=result.get('email'),
                    password=result.get('password'),
                    role=result.get('role', 'guest'),
                    phone=result.get('phone'),
                    property_name=result.get('property_name'),
                    location=result.get('location'),
                    created_at=result.get('created_at')
                )
            else:
                return User(
                    id=result[0],
                    username=result[1],
                    full_name=result[2],
                    email=result[3],
                    password=result[4],
                    role=result[5],
                    phone=result[6],
                    property_name=result[7],
                    location=result[8],
                    created_at=result[9]
                )
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_by_id(user_id):
        """Load a user by id."""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(f'''
                SELECT id, username, full_name, email, password, role, phone, property_name, location, created_at
                FROM users WHERE id = {placeholder}
            ''', (user_id,))
            
            result = cursor.fetchone()
            
            if not result:
                return None

            # Handle both dict and tuple results
            if isinstance(result, dict):
                return User(
                    id=result.get('id'),
                    username=result.get('username'),
                    full_name=result.get('full_name'),
                    email=result.get('email'),
                    password=result.get('password'),
                    role=result.get('role', 'guest'),
                    phone=result.get('phone'),
                    property_name=result.get('property_name'),
                    location=result.get('location'),
                    created_at=result.get('created_at')
                )
            else:
                return User(
                    id=result[0],
                    username=result[1],
                    full_name=result[2],
                    email=result[3],
                    password=result[4],
                    role=result[5],
                    phone=result[6],
                    property_name=result[7],
                    location=result[8],
                    created_at=result[9]
                )
        finally:
            cursor.close()
            conn.close()

    def update_profile(self, **kwargs):
        """Update user profile"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            updates = []
            values = []
            
            for key, value in kwargs.items():
                if key in ['full_name', 'phone', 'property_name', 'location']:
                    updates.append(f'{key} = {placeholder}')
                    values.append(value)
                    setattr(self, key, value)
            
            if not updates:
                return True
            
            values.append(self.id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = {placeholder}"
            
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def email_exists(email):
        """Check if email already exists"""
        return User.find_by_email(email) is not None

    @staticmethod
    def username_exists(username):
        """Check if username already exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(f'''
                SELECT id FROM users WHERE LOWER(username) = LOWER({placeholder})
            ''', (username,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'property_name': self.property_name,
            'location': self.location,
            'created_at': self.created_at
        }
