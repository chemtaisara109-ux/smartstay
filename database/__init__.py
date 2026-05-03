"""
Database connection and utilities
Improved connection handling with detailed error messages
"""
import pymysql
import sqlite3
from config import get_config

config = get_config()

# Database configuration
USE_SQLITE = config.USE_SQLITE
MAX_RETRIES = 3


def is_sqlite():
    """Return whether the current runtime database is SQLite."""
    return USE_SQLITE


def test_mysql_connection():
    """Test MySQL connection and return detailed error information"""
    try:
        print("\n" + "=" * 60)
        print("🔍 Testing MySQL Connection...")
        print("=" * 60)
        print(f"Host: {config.MYSQL_HOST}")
        print(f"Port: {config.MYSQL_PORT}")
        print(f"User: {config.MYSQL_USER}")
        print(f"Database: {config.MYSQL_DATABASE}")
        print(f"Charset: {config.MYSQL_CHARSET}")

        conn = pymysql.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
            charset=config.MYSQL_CHARSET,
            connect_timeout=config.MYSQL_TIMEOUT,
        )

        print("[OK] MySQL connection successful!")
        conn.close()
        return True
    except pymysql.Error as e:
        print(f"[ERROR] MySQL connection failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False


def get_db_connection():
    """Get database connection with retry logic"""
    global USE_SQLITE

    if USE_SQLITE:
        try:
            conn = sqlite3.connect('smartstay.db')
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"[ERROR] SQLite connection error: {e}")
            raise

    for attempt in range(MAX_RETRIES):
        try:
            conn = pymysql.connect(
                host=config.MYSQL_HOST,
                port=config.MYSQL_PORT,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE,
                charset=config.MYSQL_CHARSET,
                connect_timeout=config.MYSQL_TIMEOUT,
                cursorclass=pymysql.cursors.DictCursor,
            )
            return conn
        except pymysql.Error as e:
            print(f"[ERROR] MySQL connection attempt {attempt + 1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                import time
                time.sleep(2)
            else:
                print("[WARN] Falling back to SQLite because MySQL is unavailable.")
                USE_SQLITE = True
                try:
                    conn = sqlite3.connect('smartstay.db')
                    conn.row_factory = sqlite3.Row
                    return conn
                except sqlite3.Error as sqle:
                    print(f"[ERROR] SQLite fallback failed: {sqle}")
                    raise


def get_placeholder():
    """Get SQL placeholder based on database type"""
    return '?' if USE_SQLITE else '%s'


def _get_table_column_names(cursor, table_name):
    """Return a set of column names for a table."""
    if USE_SQLITE:
        cursor.execute(f"PRAGMA table_info({table_name})")
        return {row[1] for row in cursor.fetchall()}
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    return {row[0] for row in cursor.fetchall()}


def _ensure_user_columns(cursor):
    """Ensure host-specific columns exist on the users table."""
    columns = _get_table_column_names(cursor, 'users')

    if 'role' not in columns:
        if USE_SQLITE:
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'guest'")
        else:
            cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'guest'")

    if 'phone' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT" if USE_SQLITE else "ALTER TABLE users ADD COLUMN phone VARCHAR(20)")

    if 'property_name' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN property_name TEXT" if USE_SQLITE else "ALTER TABLE users ADD COLUMN property_name VARCHAR(200)")

    if 'location' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN location TEXT" if USE_SQLITE else "ALTER TABLE users ADD COLUMN location VARCHAR(200)")


def close_connection(conn):
    """Safely close database connection"""
    try:
        if conn:
            conn.close()
    except Exception as e:
        print(f"⚠️  Error closing connection: {e}")


def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if USE_SQLITE:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'guest',
                    phone TEXT,
                    property_name TEXT,
                    location TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            _ensure_user_columns(cursor)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    host_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    location TEXT NOT NULL,
                    price REAL NOT NULL,
                    max_guests INTEGER DEFAULT 1,
                    description TEXT,
                    image_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (host_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_verifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    property_id INTEGER NOT NULL,
                    admin_id INTEGER NOT NULL,
                    status TEXT DEFAULT 'pending',
                    notes TEXT,
                    verified_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (property_id) REFERENCES properties(id),
                    FOREIGN KEY (admin_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guest_id INTEGER NOT NULL,
                    property_id INTEGER NOT NULL,
                    guest_name TEXT NOT NULL,
                    guest_email TEXT NOT NULL,
                    guest_phone TEXT,
                    check_in DATE NOT NULL,
                    check_out DATE NOT NULL,
                    guests INTEGER NOT NULL,
                    total_price REAL NOT NULL,
                    notes TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    confirmed_at TIMESTAMP,
                    FOREIGN KEY (guest_id) REFERENCES users(id),
                    FOREIGN KEY (property_id) REFERENCES properties(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    booking_id INTEGER NOT NULL,
                    guest_id INTEGER NOT NULL,
                    property_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    review_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id),
                    FOREIGN KEY (guest_id) REFERENCES users(id),
                    FOREIGN KEY (property_id) REFERENCES properties(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS host_notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    host_id INTEGER NOT NULL,
                    booking_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (host_id) REFERENCES users(id),
                    FOREIGN KEY (booking_id) REFERENCES bookings(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS property_availability (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    property_id INTEGER NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (property_id) REFERENCES properties(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS password_resets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    token TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    used INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS remember_tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    token TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    full_name VARCHAR(100) NOT NULL,
                    email VARCHAR(120) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) DEFAULT 'guest',
                    phone VARCHAR(20),
                    property_name VARCHAR(200),
                    location VARCHAR(200),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    host_id INT NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    location VARCHAR(200) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    max_guests INT DEFAULT 1,
                    description TEXT,
                    image_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (host_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_verifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    property_id INT NOT NULL,
                    admin_id INT NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    notes TEXT,
                    verified_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (property_id) REFERENCES properties(id),
                    FOREIGN KEY (admin_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    guest_id INT NOT NULL,
                    property_id INT NOT NULL,
                    guest_name VARCHAR(100) NOT NULL,
                    guest_email VARCHAR(120) NOT NULL,
                    guest_phone VARCHAR(20),
                    check_in DATE NOT NULL,
                    check_out DATE NOT NULL,
                    guests INT NOT NULL,
                    total_price DECIMAL(10,2) NOT NULL,
                    notes TEXT,
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    confirmed_at TIMESTAMP NULL,
                    FOREIGN KEY (guest_id) REFERENCES users(id),
                    FOREIGN KEY (property_id) REFERENCES properties(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    booking_id INT NOT NULL,
                    guest_id INT NOT NULL,
                    property_id INT NOT NULL,
                    rating INT NOT NULL,
                    review_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id),
                    FOREIGN KEY (guest_id) REFERENCES users(id),
                    FOREIGN KEY (property_id) REFERENCES properties(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS host_notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    host_id INT NOT NULL,
                    booking_id INT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (host_id) REFERENCES users(id),
                    FOREIGN KEY (booking_id) REFERENCES bookings(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS property_availability (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    property_id INT NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (property_id) REFERENCES properties(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS password_resets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    token VARCHAR(255) NOT NULL,
                    expires_at DATETIME NOT NULL,
                    used BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS remember_tokens (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    token VARCHAR(255) NOT NULL,
                    expires_at DATETIME NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON users(email)')

        conn.commit()
        print("[OK] Database tables initialized successfully")
        
        # Insert sample data
        insert_sample_data(conn)
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Error initializing database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def insert_sample_data(conn):
    """Insert sample data for testing"""
    cursor = conn.cursor()
    
    try:
        # Import User model to properly hash passwords
        from models.user_enhanced import User
        
        # Check if sample user exists
        if USE_SQLITE:
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = 'guest@smartstay.com'")
        else:
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = 'guest@smartstay.com'")
        
        if cursor.fetchone()[0] == 0:
            # Create guest user with password: Guest@1234
            guest_hashed_password = User.hash_password('Guest@1234')
            
            if USE_SQLITE:
                cursor.execute('''
                    INSERT INTO users (username, full_name, email, password, role, created_at)
                    VALUES (?, ?, ?, ?, ?, datetime('now'))
                ''', ('testguest', 'Test Guest', 'guest@smartstay.com', guest_hashed_password, 'guest'))
            else:
                cursor.execute('''
                    INSERT INTO users (username, full_name, email, password, role)
                    VALUES (%s, %s, %s, %s, %s)
                ''', ('testguest', 'Test Guest', 'guest@smartstay.com', guest_hashed_password, 'guest'))
            
            guest_id = cursor.lastrowid
            
            # Create host user with password: Host@1234
            host_hashed_password = User.hash_password('Host@1234')
            
            if USE_SQLITE:
                cursor.execute('''
                    INSERT INTO users (username, full_name, email, password, role, phone, property_name, location, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                ''', ('samplehost', 'Sample Host', 'host@smartstay.com', host_hashed_password, 'host', '+1-555-0123', 'Sample Properties LLC', 'California'))
            else:
                cursor.execute('''
                    INSERT INTO users (username, full_name, email, password, role, phone, property_name, location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', ('samplehost', 'Sample Host', 'host@smartstay.com', host_hashed_password, 'host', '+1-555-0123', 'Sample Properties LLC', 'California'))
            
            host_id = cursor.lastrowid
            
            # Insert sample properties
            sample_properties = [
                ('Cozy Downtown Apartment', 'New York, NY', 150.00, 2, 'A beautiful apartment in the heart of the city with stunning views.'),
                ('Beachfront Villa', 'Miami, FL', 300.00, 4, 'Luxurious villa right on the beach with private pool and ocean access.'),
                ('Mountain Cabin', 'Asheville, NC', 120.00, 3, 'Rustic cabin in the mountains, perfect for a weekend getaway.'),
                ('Urban Loft', 'Chicago, IL', 180.00, 2, 'Modern loft in the trendy neighborhood with city views.'),
                ('Lake House', 'Lake Tahoe, CA', 250.00, 6, 'Spacious lake house with boat dock and mountain views.')
            ]
            
            for title, location, price, max_guests, description in sample_properties:
                if USE_SQLITE:
                    cursor.execute('''
                        INSERT INTO properties (host_id, title, location, price, max_guests, description)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (host_id, title, location, price, max_guests, description))
                else:
                    cursor.execute('''
                        INSERT INTO properties (host_id, title, location, price, max_guests, description)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (host_id, title, location, price, max_guests, description))
            
            conn.commit()
            print("[OK] Sample data inserted successfully")
            print("[INFO] Test User Credentials:")
            print("   Guest Email: guest@smartstay.com")
            print("   Guest Password: Guest@1234")
            print("   Host Email: host@smartstay.com")
            print("   Host Password: Host@1234")
        else:
            print("[INFO] Sample data already exists")
            
    except Exception as e:
        print(f"[WARN] Error inserting sample data: {e}")
        conn.rollback()
